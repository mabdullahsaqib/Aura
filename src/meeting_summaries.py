import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import whisper
from firebase_admin import firestore
from config import GEMINI_API_KEY

# Initialize recognizer and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 250)  # Adjust speaking rate if needed

# Initialize Firestore
db = firestore.client()

# Initialize GEMINI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

whisper_model = None
# Initialize Whisper Model
def load_model():
    whisper_model = whisper.load_model("base")


# Transcribe Audio Function
def transcribe_audio(file_path):
    result = whisper_model.transcribe(file_path)
    transcript = result['text']
    print("Transcript : ", transcript)
    return transcript


# Summarize Transcript with GEMINI
def summarize_text(text):
    response = model.generate_content("Summarize the following meeting transcript, briefly :" + text)
    print("Summary : ", response.text)
    return response.text


# Store Meeting Summary in Firestore
def store_summary(meeting_title, transcript, summary):
    doc_ref = db.collection("meeting_summaries").document(meeting_title)
    doc_ref.set({
        "title": meeting_title,
        "transcript": transcript,
        "summary": summary
    })
    print(f"Meeting '{meeting_title}' summary saved successfully.")


# Main Function to Transcribe, Summarize, and Store
def process_meeting_summary(file_path, meeting_title):
    load_model()
    print("Transcribing audio...")
    transcript = transcribe_audio(file_path)
    print("Transcription complete. Summarizing text...")
    summary = summarize_text(transcript)
    print("Summary complete. Storing in Firestore...")
    store_summary(meeting_title, transcript, summary)
    with open(f"{meeting_title}_summary.txt", "w") as file:
        file.write(summary)
    print(f"Meeting summary for '{meeting_title}' processed and stored.")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        while True:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio)
                print("Command : " + command )
                return command
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                speak("Voice service unavailable.")
                return ""


def meeting_summary_voice_interaction():
    """
    Handles the meeting summary command.
    Asks user for the audio file and processes the meeting summary.
    """

    speak("What's the name of the audio file?")
    audio_file = listen()
    if audio_file:
        speak(f"Processing the meeting summary from the file located at {audio_file}.")
        title = "Meeting Summary"
        process_meeting_summary(audio_file, title)
        speak("The meeting summary has been processed and stored.")
    else:
        speak("Sorry, I couldn't process the audio file. Please try again.")


# Example Usage
if __name__ == "__main__":
    meeting_summary_voice_interaction()
