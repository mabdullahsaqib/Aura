import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from datetime import datetime
from task_management import add_task_from_input, get_tasks_by_priority, get_upcoming_tasks
from web_browsing import search_web, open_link
from note_taking import add_note, retrieve_all_notes, retrieve_notes, delete_note
from document_management import create_document, retrieve_document, delete_document, classify_document, move_document
from email_management import fetch_emails, send_email
from weather_and_news import get_weather, get_news
from personalized_recommendations import recommend_news, recommend_tasks, general_recommendations
from config import GEMINI_API_KEY

# Initialize models and recognizer
genai.configure(api_key=GEMINI_API_KEY)
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust voice rate

# Text-to-Speech
def speak(text):
    print("Aura:", text)  # Also print for reference
    engine.say(text)
    engine.runAndWait()

# Voice-to-Text
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

# Command Execution
def execute_command(command):
    command = command.lower()

    # Task Management
    if "task" in command:
        if "add task" in command:
            speak("What's the task description?")
            task_desc = listen()
            speak("What's the deadline? (e.g., 2024-11-12 14:00)")
            deadline_str = listen()
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            add_task_from_input(task_desc, deadline)
            speak(f"Task '{task_desc}' added.")
        elif "show tasks" in command:
            tasks = get_tasks_by_priority("high")
            speak("Here are your high-priority tasks.")
            for task in tasks:
                speak(task.get("description", "Task"))

    # Web Browsing and Research
    elif "search" in command:
        speak("What would you like to search for?")
        query = listen()
        results = search_web(query)
        for idx, res in enumerate(results):
            speak(f"Result {idx+1}: {res['title']}")
        speak("Would you like to open a link?")
        response = listen()
        if "yes" in response:
            open_link(results[0]["link"])  # Opens the first link by default

    # Note-Taking
    elif "note" in command:
        if "add note" in command:
            speak("What's the note title?")
            title = listen()
            speak("What's the note content?")
            content = listen()
            add_note(title, content)
            speak("Note added.")
        elif "show notes" in command:
            notes = retrieve_all_notes()
            for note in notes:
                speak(f"Note ID: {note.id}, Title: {note['title']}")
        elif "read note" in command:
            speak("Please provide the note ID.")
            note_id = listen()
            note = retrieve_note(note_id)
            speak(f"Content: {note['content']}")

    # Document Management
    elif "document" in command:
        if "create document" in command:
            speak("Provide the document title.")
            title = listen()
            speak("Provide the document content.")
            content = listen()
            create_document(title, content)
            speak("Document created.")
        elif "delete document" in command:
            speak("Provide the document name to delete.")
            doc_name = listen()
            delete_document(doc_name)
            speak("Document deleted.")

    # Email Management
    elif "email" in command:
        if "check emails" in command:
            emails = fetch_emails()
            for email in emails:
                speak(f"From: {email['from']}, Subject: {email['subject']}")
        elif "send email" in command:
            speak("To whom should I send the email?")
            recipient = listen()
            speak("What should the subject be?")
            subject = listen()
            speak("What should I say in the email?")
            body = listen()
            send_email(recipient, subject, body)
            speak("Email sent.")

    # Weather and News Updates
    elif "weather" in command:
        speak("For which location?")
        location = listen()
        weather = get_weather(location)
        speak(f"Weather in {location}: {weather}")
    elif "news" in command:
        speak("Fetching top news.")
        news = get_news()
        for item in news:
            speak(f"Headline: {item['title']}")

    # Recommendations
    elif "recommendation" in command:
        speak("Fetching personalized recommendations.")
        news = recommend_news("example_user")
        speak(f"Recommended news: {news}")
        tasks = recommend_tasks("example_user")
        speak(f"Urgent tasks: {tasks}")

    else:
        speak("Command not recognized. Please try again.")

# Main Interaction Loop
def main():
    speak("Voice interaction initialized. Awaiting your command.")
    while True:
        command = listen()
        if command:
            if "exit" in command or "stop" in command:
                speak("Shutting down voice interaction.")
                break
            execute_command(command)

if __name__ == "__main__":
    main()
