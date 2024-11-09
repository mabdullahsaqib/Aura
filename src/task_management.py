import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
from datetime import datetime
import dateparser
import speech_recognition as sr
import pyttsx3
from config import FIREBASE_CREDENTIALS_PATH, GEMINI_API_KEY

# Initialize Firestore
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize recognizer and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Voice service unavailable.")
        return ""


# Function to infer priority and category using Gemini
def infer_task_details(task_description):
    response = model.generate_content(
        f"What is the priority and category of this task? Only provide the priority (high,medium,low) as priority : and category (work, personal) as category : , nothing else, no description, no extra information. : {task_description}"
    )
    return response.text.lower()


def add_task_from_input(task_description, deadline):
    inferred_details = infer_task_details(task_description)
    priority = "medium"
    category = "personal"

    if "priority" in inferred_details and "category" in inferred_details:
        priority = "high" if "high" in inferred_details else "low" if "low" in inferred_details else "medium"
        category = "work" if "work" in inferred_details else "personal"

    task_data = {
        "title": task_description,
        "category": category,
        "deadline": deadline,
        "priority": priority,
        "created_at": datetime.now(),
    }

    db.collection("tasks").add(task_data)
    speak(f"Task '{task_description}' added with priority: {priority} and category: {category}")


def get_tasks_by_priority(priority):
    tasks = db.collection("tasks").where("priority", "==", priority).stream()
    task_list = [task.to_dict() for task in tasks]

    speak(f"Tasks with priority '{priority}':")
    for task in task_list:
        speak(f"{task['title']} with deadline on {task['deadline']}")
    return task_list


def get_tasks_by_category(category):
    tasks = db.collection("tasks").where("category", "==", category).stream()
    task_list = [task.to_dict() for task in tasks]

    speak(f"Tasks in category '{category}':")
    for task in task_list:
        speak(f"{task['title']} with priority {task['priority']}")
    return task_list


def get_upcoming_tasks(deadline_date):
    tasks = db.collection("tasks").where("deadline", "<=", deadline_date).order_by("deadline").stream()
    upcoming_tasks = [task.to_dict() for task in tasks]

    speak("Here are the upcoming tasks:")
    for task in upcoming_tasks:
        speak(f"{task['title']} with deadline on {task['deadline']}")
    return upcoming_tasks


def task_voice_interaction():
    speak(
        "Task Management module activated. You can add a task, get tasks by priority, category, or view upcoming tasks. Say 'exit' to leave.")
    while True:
        command = listen().lower()

        if "add task" in command:
            speak("What is the task description?")
            task_description = listen()
            speak("What is the deadline?")
            deadline_input = listen()
            deadline = dateparser.parse(deadline_input) if deadline_input else None
            add_task_from_input(task_description, deadline)

        elif "priority" in command:
            speak("What priority level would you like to check? (high, medium, low)")
            priority = listen()
            get_tasks_by_priority(priority.lower())

        elif "category" in command:
            speak("Which category would you like to check? (work or personal)")
            category = listen()
            get_tasks_by_category(category.lower())

        elif "upcoming" in command:
            speak("Specify the deadline for upcoming tasks.")
            deadline_input = listen()
            deadline_date = dateparser.parse(deadline_input)
            get_upcoming_tasks(deadline_date)

        elif "exit" in command:
            speak("Exiting Task Management module.")
            break
        else:
            speak("Sorry, I didn't understand that command.")


# Example Usage
if __name__ == "__main__":
    task_voice_interaction()
