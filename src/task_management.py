import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
from datetime import datetime
from config import FIREBASE_CREDENTIALS_PATH , GEMINI_API_KEY
import dateparser

# Initialize Firestore
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to infer priority and category using Gemini
def infer_task_details(task_description):
    # Call Gemini to infer priority and category

    response = model.generate_content(f"What is the priority and category of this task? Only provide the priority (high,medium,low) as priority : and category (work, personal) as category : , nothing else, no description, no extra information. : {task_description}")
    print(response.text)
    # Assuming Gemini provides a response like "Priority: high, Category: work"
    return response.text.lower()


# Function to add a new task
def add_task_from_input(task_description, deadline):
    """
        Add a new task to the Firestore 'tasks' collection.

        Parameters:
            title (str): The task description.
            category (str): The task category, e.g., 'work' or 'personal'.
            deadline (datetime): The deadline for the task.
            priority (str): The priority level of the task (high, medium, low).
    """

    # Call Gemini to infer the task's priority and category
    inferred_details = infer_task_details(task_description)

    # If no response from Gemini or parsing error, use default values
    if "priority" not in inferred_details or "category" not in inferred_details:
        priority = "medium"
        category = "personal"
    else:
        # Extract inferred priority and category from Gemini's response
        priority = "high" if "high" in inferred_details else "low" if "low" in inferred_details else "medium"
        category = "work" if "work" in inferred_details else "personal"

    # Create the task with inferred or default details
    task_data = {
        "title": task_description,
        "category": category,
        "deadline": deadline,
        "priority": priority,
        "created_at": datetime.now(),
    }

    # Add task to the 'tasks' collection in Firestore
    db.collection("tasks").add(task_data)
    print(f"Task '{task_description}' added with priority: {priority} and category: {category}")


# Function to retrieve tasks by priority
def get_tasks_by_priority(priority):
    """
    Retrieve tasks from the Firestore 'tasks' collection by priority.

    Parameters:
        priority (str): The priority level to filter by, e.g., 'high', 'medium', or 'low'.

    Returns:
        list: A list of tasks with the specified priority.
    """
    tasks = db.collection("tasks").where("priority", "==", priority).stream()
    task_list = [task.to_dict() for task in tasks]

    print(f"Tasks with priority '{priority}':")
    for task in task_list:
        print(f"- {task['title']} (Deadline: {task['deadline']}, Category: {task['category']})")

    return task_list

# Function to retrieve tasks by category
def get_tasks_by_category(category):
    """
    Retrieve tasks from the Firestore 'tasks' collection by category.

    Parameters:
        category (str): The category level to filter by, e.g., 'work' or 'personal'.

    Returns:
        list: A list of tasks with the specified category.
    """
    tasks = db.collection("tasks").where("category", "==", category).stream()
    task_list = [task.to_dict() for task in tasks]

    print(f"Tasks with category '{category}':")
    for task in task_list:
        print(f"- {task['title']} (Deadline: {task['deadline']}, Priority: {task['priority']})")

    return task_list

# Function to retrieve tasks by deadline
def get_upcoming_tasks(deadline_date):
    """
    Retrieve tasks that are due before a specified deadline date.

    Parameters:
        deadline_date (datetime): The cutoff date for upcoming tasks.

    Returns:
        list: A list of upcoming tasks.
    """
    tasks = db.collection("tasks").where("deadline", "<=", deadline_date).order_by("deadline").stream()
    upcoming_tasks = [task.to_dict() for task in tasks]

    print("Upcoming tasks:")
    for task in upcoming_tasks:
        print(f"- {task['title']} (Deadline: {task['deadline']}, Priority: {task['priority']}, Category: {task['category']})")

    return upcoming_tasks

# Function to prompt for user input
def get_user_input():
    task_description = input("What is the task? ")
    deadline_input = input("When is the deadline? (e.g., 'tomorrow at 5 PM', leave blank if no deadline): ")

    # Parse the deadline if provided
    if deadline_input.strip():
        deadline = dateparser.parse(deadline_input)
        if not deadline:
            print("Couldn't parse the deadline. Please try again with a specific format.")
            return None, None
    else:
        deadline = None  # No deadline specified

    return task_description, deadline

# Example Usage
if __name__ == "__main__":

    task_description, deadline = get_user_input()
    if task_description and deadline:
        add_task_from_input(task_description, deadline)

    # Retrieve high-priority tasks
    high_priority_tasks = get_tasks_by_priority("high")
    category_tasks = get_tasks_by_category("work")

    # Retrieve upcoming tasks with a deadline before a certain date
    upcoming_tasks = get_upcoming_tasks(datetime(2024, 11, 12))
