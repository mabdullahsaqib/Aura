import os
import shutil
from pathlib import Path
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
from firebase_admin import firestore
from config import GEMINI_API_KEY

# Initialize recognizer and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 250)  # Adjust speaking rate if needed

# Initialize Firestore
db = firestore.client()

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Common folders as base directories for searches
COMMON_FOLDERS = {
    "documents": Path.home() / "Documents",
    "downloads": Path.home() / "Downloads",
    "desktop": Path.home() / "Desktop",
    "pictures": Path.home() / "Pictures",
    "videos": Path.home() / "Videos",
    "music": Path.home() / "Music",
}


def create_document(file_name, content, base_folder_name, target_folder_name):
    """
    Creates a new document with the specified content.

    Parameters:
        file_name (str): The name of the file to create.
        content (str): The content to write to the file.
    """
    base_directory = COMMON_FOLDERS.get(base_folder_name.lower(), Path(base_folder_name))

    if not base_directory.exists():
        print(f"Base directory '{base_directory}' does not exist.")
        return

    if base_folder_name == target_folder_name:
        target_path = base_directory
    else:
        # Search for the target folder within the base directory
        target_path = find_folder(base_directory, target_folder_name)

    if target_path:
        file_path = target_path / file_name
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Document '{file_name}' created in '{target_path}'.")


def edit_document(file_name, new_content, base_folder_name, target_folder_name):
    """
    Edits an existing document by appending new content.

    Parameters:
        file_name (str): The name of the file to edit.
        new_content (str): The new content to append.
    """
    base_directory = COMMON_FOLDERS.get(base_folder_name.lower(), Path(base_folder_name))

    if not base_directory.exists():
        print(f"Base directory '{base_directory}' does not exist.")
        return

    if base_folder_name == target_folder_name:
        target_path = base_directory
    else:
        # Search for the target folder within the base directory
        target_path = find_folder(base_directory, target_folder_name)

    if target_path:
        file_path = target_path / file_name
        if file_path.exists():
            with open(file_path, 'w') as file:
                file.write(new_content)
            print(f"Document '{file_name}' edited successfully.")
        else:
            print(f"Document '{file_name}' not found in '{target_path}'.")


def delete_document(file_name, base_folder_name, target_folder_name):
    """
    Deletes a document.

    Parameters:
        file_name (str): The name of the file to delete.
    """
    base_directory = COMMON_FOLDERS.get(base_folder_name.lower(), Path(base_folder_name))

    if not base_directory.exists():
        print(f"Base directory '{base_directory}' does not exist.")
        return

    if base_folder_name == target_folder_name:
        target_path = base_directory
    else:
        # Search for the target folder within the base directory
        target_path = find_folder(base_directory, target_folder_name)

    if target_path:
        file_path = target_path / file_name
        if file_path.exists():
            file_path.unlink()
            print(f"Document '{file_name}' deleted from '{target_path}'.")
        else:
            print(f"Document '{file_name}' not found in '{target_path}'.")


def summarize_document(file_name, base_folder_name, target_folder_name):
    """
    Summarizes the content of a document using Gemini.

    Parameters:
        file_name (str): The name of the file to summarize.

    Returns:
        str: The summary of the document.
    """
    base_directory = COMMON_FOLDERS.get(base_folder_name.lower(), Path(base_folder_name))

    if not base_directory.exists():
        print(f"Base directory '{base_directory}' does not exist.")
        return

    if base_folder_name == target_folder_name:
        target_path = base_directory
    else:
        # Search for the target folder within the base directory
        target_path = find_folder(base_directory, target_folder_name)

    if target_path:
        file_path = target_path / file_name

        if file_path.exists():
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()
            response = model.generate_content("Summarize the following file content: " + content)
            return response.text

        else:
            print(f"Document '{file_name}' not found in {target_path}.")
            return None


def classify_document(file_name, base_folder_name, target_folder_name):
    """
    Classifies a document based on its content using Gemini.

    Parameters:
        file_name (str): The name of the file to classify.

    Returns:
        str: The classification of the document.
    """
    base_directory = COMMON_FOLDERS.get(base_folder_name.lower(), Path(base_folder_name))

    if not base_directory.exists():
        print(f"Base directory '{base_directory}' does not exist.")
        return

    if base_folder_name == target_folder_name:
        target_path = base_directory
    else:
        # Search for the target folder within the base directory
        target_path = find_folder(base_directory, target_folder_name)

    if target_path:
        file_path = target_path / file_name
        if file_path.exists():
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()

            response = model.generate_content(
                "Classify this file content to a category, say only work or personal: " + content)
            print(f"Document '{file_name}' classified as: {response.text.strip()}")
            return response.text.strip()

        else:
            print(f"Document '{file_name}' not found in {target_path}.")
            return None


def retrieve_document(document_name, base_folder_name, target_folder_name):
    """
    Retrieves the path of a specific document within a target folder in a base folder.

    Parameters:
        base_folder_name (str): The name of the base folder to start searching from.
        target_folder_name (str): The name of the folder containing the document.
        document_name (str): The name of the document to retrieve.

    Returns:
        Path: The path of the document if found, or None if not found.
    """

    base_directory = COMMON_FOLDERS.get(base_folder_name.lower(), Path(base_folder_name))

    if not base_directory.exists():
        print(f"Base directory '{base_directory}' does not exist.")
        return

    if base_folder_name == target_folder_name:
        target_path = base_directory
    else:
        # Search for the target folder within the base directory
        target_path = find_folder(base_directory, target_folder_name)

    if target_path:
        document_path = target_path / document_name
        if document_path.exists():
            try:
                with open(document_path, "r") as file:
                    content = file.read()
                print(f"\nContent of '{document_name}':\n{content}")
                return content

            except FileNotFoundError:
                print(f"Document '{document_name}' not found at {target_path}.")
                return None

        else:
            print(f"Document '{document_name}' not found in '{target_path}'.")
            return None


def find_folder(base_directory, target_folder_name):
    """
    Recursively searches for a folder by name starting from a base directory.

    Parameters:
        base_directory (Path): The directory to start searching from.
        target_folder_name (str): The name of the folder to search for.

    Returns:
        Path: The full path to the target folder if found, or None if not found.
    """
    for root, dirs, _ in os.walk(base_directory):
        for dir_name in dirs:
            if dir_name.lower() == target_folder_name.lower():
                return Path(root) / dir_name
    print(f"Folder '{target_folder_name}' not found in '{base_directory}'.")
    return None


def move_document(file_name, current_base_folder_name, current_folder_name, target_base_folder_name,
                  target_folder_name):
    """
    Moves a document to a target folder, searching within a base folder.

    Parameters:
        file_name (str): The name of the file to move.
        base_folder_name (str): The name of the base folder to start searching from.
        target_folder_name (str): The name of the folder to move the file into.
    """

    current_base_directory = COMMON_FOLDERS.get(current_base_folder_name.lower(), Path(current_base_folder_name))

    if not current_base_directory.exists():
        print(f"Base directory '{current_base_directory}' does not exist.")
        return

    if current_base_folder_name == current_folder_name:
        file_path = current_base_directory / file_name
    else:
        # search for the file in the current folder
        current_path = find_folder(current_base_directory, current_folder_name)
        if current_path:
            file_path = current_path / file_name
        else:
            print(f"Document '{file_name}' not found in '{current_base_directory}'.")
            return

    target_base_directory = COMMON_FOLDERS.get(target_base_folder_name.lower(), Path(target_base_folder_name))

    if not target_base_directory.exists():
        print(f"Base directory '{target_base_directory}' does not exist.")
        return

    if target_base_folder_name == target_folder_name:
        target_path = target_base_directory
    else:
        # Search for the target folder within the base directory
        target_path = find_folder(target_base_directory, target_folder_name)

    if target_path:
        try:
            shutil.move(file_path, target_path / Path(file_name).name)
            print(f"Document '{file_name}' moved to '{target_path}' successfully.")
        except FileNotFoundError:
            print(f"Document '{file_name}' not found.")
        except Exception as e:
            print(f"An error occurred while moving the document: {e}")
    else:
        print(f"Target folder '{target_folder_name}' not found.")


def list_documents(base_folder_name, target_folder_name):
    """
    Lists all documents in a target folder within a specified base folder.

    Parameters:
        base_folder_name (str): The name of the base folder to start searching from.
        target_folder_name (str): The name of the folder to list documents from.

    Returns:
        list: A list of document paths within the target folder.
    """
    base_directory = COMMON_FOLDERS.get(base_folder_name.lower(), Path(base_folder_name))

    if not base_directory.exists():
        print(f"Base directory '{base_directory}' does not exist.")
        return

    if base_folder_name == target_folder_name:
        target_path = base_directory
    else:
        # Search for the target folder within the base directory
        target_path = find_folder(base_directory, target_folder_name)

    if target_path and target_path.exists():
        documents = [file for file in target_path.iterdir() if file.is_file()]
        print(f"Documents in '{target_path}':")
        for doc in documents:
            print(doc.name)
        return documents
    else:
        print(f"Target folder '{target_folder_name}' not found.")
        return []


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        while True:
            audio = recognizer.listen(source, timeout=3)
            try:
                return recognizer.recognize_google(audio)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                speak("I didn't catch that.")
                continue
            except sr.RequestError:
                speak("Voice service unavailable.")
                return ""

def document_management_voice_interaction(command):
    if "create" in command:
        speak("What is the name of the file?")
        file_name = listen().lower()
        speak("What content would you like to add to the file?")
        content = listen().lower()
        speak("Which base folder is the target folder in?")
        base_folder = listen().lower()
        speak("What target folder should I use?")
        target_folder = listen().lower()
        create_document(file_name, content, base_folder, target_folder)
        speak(f"Document {file_name} created successfully.")

    elif "edit" in command:
        speak("What is the name of the file to edit?")
        file_name = listen().lower()
        speak("What new content would you like to append?")
        new_content = listen().lower()
        speak("Which base folder is the target folder or document in?")
        base_folder = listen().lower()
        speak("What target folder is this document in?")
        target_folder = listen().lower()
        edit_document(file_name, new_content, base_folder, target_folder)
        speak(f"Document {file_name} edited successfully.")

    elif "delete" in command:
        speak("What is the name of the file to delete?")
        file_name = listen().lower()
        speak("Which base folder is the target folder or this document in?")
        base_folder = listen().lower()
        speak("What target folder is this document in?")
        target_folder = listen().lower()
        delete_document(file_name, base_folder, target_folder)
        speak(f"Document {file_name} deleted successfully.")

    elif "summarize" in command:
        speak("What is the name of the file to summarize?")
        file_name = listen().lower()
        speak("Which base folder is this document in?")
        base_folder = listen().lower()
        speak("What target folder is this document in?")
        target_folder = listen().lower()
        summary = summarize_document(file_name, base_folder, target_folder)
        speak(f"The summary of {file_name} is: {summary}")

    elif "classify" in command:
        speak("What is the name of the file to classify?")
        file_name = listen().lower()
        speak("Which base folder is this document in?")
        base_folder = listen().lower()
        speak("What target folder is this document in?")
        target_folder = listen().lower()
        classify_document(file_name, base_folder, target_folder)
        speak(f"Document {file_name} classified successfully.")

    elif "move" in command:
        speak("What is the name of the file to move?")
        file_name = listen().lower()
        speak("Which current base folder is this file in?")
        current_base_folder = listen().lower()
        speak("Which current folder is this file in?")
        current_folder = listen().lower()
        speak("Which target base folder should this file move to?")
        target_base_folder = listen().lower()
        speak("Which target folder should this file move to?")
        target_folder = listen().lower()
        move_document(file_name, current_base_folder, current_folder, target_base_folder, target_folder)
        speak(f"Document {file_name} moved successfully.")

    elif "retrieve" in command:
        speak("What is the name of the document to retrieve?")
        document_name = listen().lower()
        speak("Which base folder is the target folder or document in?")
        base_folder = listen().lower()
        speak("What target folder is this document in?")
        target_folder = listen().lower()
        retrieve_document(document_name, base_folder, target_folder)
        speak(f"Document {document_name} retrieved successfully.")

    elif "list" in command:
        speak("Which base folder would you like to list documents from?")
        base_folder = listen().lower()
        speak("Which target folder would you like to list documents from?")
        target_folder = listen().lower()
        list_documents(base_folder, target_folder)
        speak("Listing documents complete.")

    else:
        speak("I didn't understand that command. Please try again.")
