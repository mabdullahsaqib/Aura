import speech_recognition as sr
import pyttsx3
import random

# Import all the modules as needed
from task_management import task_voice_interaction
from web_browsing import web_browsing_voice_interaction
from note_taking import note_voice_interaction
from document_management import document_management_voice_interaction
from custom_commands import check_and_execute_command
from realtime_translation import translation_voice_interaction
from email_management import email_voice_interaction
from weather_and_news import weather_and_news_voice_interaction
from personalized_recommendations import recommendations_voice_interaction
from entertainment_controls import entertainment_control_voice_interaction
from meeting_summaries import meeting_summary_voice_interaction


# Initialize recognizer and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking rate if needed

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

def activate_module(command):
    """
    Activate the appropriate module based on the user's command.
    """
    if "task" in command:
        task_voice_interaction(command)
    elif "web" in command or "search" in command or "browse" in command:
        web_browsing_voice_interaction(command)
    elif "note" in command:
        note_voice_interaction(command)
    elif "document" in command or "file" in command or "folder" in command or "directory" in command or "drive" in command:
        document_management_voice_interaction(command)
    elif "translation" in command or "translate" in command :
        translation_voice_interaction()
    elif "email" in command or "mail" in command or "inbox" in command :
        email_voice_interaction(command)
    elif "weather" in command or "news" in command or "headline" in command or "article" in command :
        weather_and_news_voice_interaction(command)
    elif "recommendation" in command or "suggestion" in command or "advice" in command or "recommendations" in command or "recommend" in command:
        recommendations_voice_interaction(command)
    elif "entertainment" in command or "music" in command or "video" in command or "movie" in command or "spotify" in command or "youtube" in command:
        entertainment_control_voice_interaction()
    elif "meeting" in command or "summary" in command or "transcript" in command:
        meeting_summary_voice_interaction(command)
    else:
        check_and_execute_command(command)

def main():
    """
    Main function to handle voice commands and activate modules.
    """
    greetings = ["Hello!", "Hi!", "Hey there!", "Greetings!", "Good day!", "Hello, how can I assist you today?"]
    speak(random.choice(greetings))

    while True:
        command = listen()
        if "exit" in command.lower():
            speak("Goodbye!")
            break
        activate_module(command.lower())

