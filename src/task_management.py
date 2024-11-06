import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from config import FIREBASE_CREDENTIALS_PATH

# Initialize Firestore
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()


# Function to add a new task
def add_task(title, category, deadline, priority):
    """
    Add a new task to the Firestore 'tasks' collection.

    Parameters:
        title (str): The task description.
        category (str): The task category, e.g., 'work' or 'personal'.
        deadline (datetime): The deadline for the task.
        priority (str): The priority level of the task (high, medium, low).
    """
    task_data = {
        "title": title,
        "category": category,
        "deadline": deadline,
        "priority": priority,
        "created_at": datetime.now(),
    }

    # Add task to the 'tasks' collection
    db.collection("tasks").add(task_data)
    print(f"Task '{title}' added successfully.")


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
        print(f"- {task['title']} (Deadline: {task['deadline']}, Priority: {task['priority']})")

    return upcoming_tasks


# Example Usage
if __name__ == "__main__":
    # Add a task
    add_task(
        title="Finish project proposal",
        category="work",
        deadline=datetime(2024, 11, 10, 17, 0),
        priority="low"
    )

    # Retrieve high-priority tasks
    high_priority_tasks = get_tasks_by_priority("high")

    # Retrieve upcoming tasks with a deadline before a certain date
    upcoming_tasks = get_upcoming_tasks(datetime(2024, 11, 12))
