from googletrans import Translator
import speech_recognition as sr
import pyttsx3


# Initialize recognizer and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking rate if needed

# Initialize the translator
translator = Translator()


def translate_text(text, target_language="en"):
    """
    Translates text to a specified target language.

    Parameters:
        text (str): The text to translate.
        target_language (str): The language code to translate the text to (e.g., "en" for English, "fr" for French).

    Returns:
        str: The translated text.
    """
    try:
        # Detect the original language
        detected_language = translator.detect(text).lang
        print(f"Detected language: {detected_language}")

        # Translate the text to the target language
        translated = translator.translate(text, dest=target_language)
        print(f"Translated to {target_language}: {translated.text}")

        return translated.text

    except Exception as e:
        print(f"Error during translation: {e}")
        return None

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


def translation_voice_interaction():
    """
    Main function to interact with the Real-Time Translation system.
    It listens for input in one language and translates it to another language.
    """
    speak("Real-Time Translation - Say 'exit' to quit.")

    while True:
        speak("\nPlease say something to translate...")
        text_to_translate = listen()

        if text_to_translate.lower() == "exit":
            print("Exiting Real-Time Translation.")
            break

        print(f"Original Text: {text_to_translate}")

        # Ask the user for the target language
        target_language = "en"

        translated_text = translate_text(text_to_translate, target_language)
        print("Translated Text : " + translated_text)
        speak(translated_text)
