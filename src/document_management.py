import os
import shutil
from pathlib import Path
import google.generativeai as genai
from config import GEMINI_API_KEY

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
            response = model.generate_content("Summarize the following file content: " + content )
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

            response = model.generate_content("Classify this file content to a category, say only work or personal: " + content)
            print(f"Document '{file_name}' classified as: {response.text.strip()}")
            return response.text.strip()

        else:
            print(f"Document '{file_name}' not found in {target_path}.")
            return None


def retrieve_document(base_folder_name, target_folder_name, document_name):
    """
    Retrieves the path of a specific document within a target folder in a base folder.

    Parameters:
        base_folder_name (str): The name of the base folder to start searching from.
        target_folder_name (str): The name of the folder containing the document.
        document_name (str): The name of the document to retrieve.

    Returns:
        Path: The path of the document if found, or None if not found.
    """
    documents = list_documents(base_folder_name, target_folder_name)
    for doc in documents:
        if doc.name.lower() == document_name.lower():
            print(f"Document '{document_name}' found at '{doc}'.")
            return doc
    print(f"Document '{document_name}' not found in '{target_folder_name}'.")
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


def move_document(file_name, base_folder_name, target_folder_name):
    """
    Moves a document to a target folder, searching within a base folder.

    Parameters:
        file_name (str): The name of the file to move.
        base_folder_name (str): The name of the base folder to start searching from.
        target_folder_name (str): The name of the folder to move the file into.
    """
    # Get the base directory path from COMMON_FOLDERS
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
        try:
            shutil.move(file_name, target_path / Path(file_name).name)
            print(f"Document '{file_name}' moved to '{target_path}' successfully.")
        except FileNotFoundError:
            print(f"Document '{file_name}' not found.")
        except Exception as e:
            print(f"An error occurred while moving the document: {e}")
    else:
        print(f"Target folder '{target_folder_name}' could not be located within '{base_directory}'.")


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


def main():
    """
    Main function to interact with the Document Management Module.
    """
    print("Welcome to Aura's Document Management Module!")
    while True:
        choice = input("\nChoose an option: [create, edit, delete, summarize, classify, move, retrieve, list, exit]: ").lower()

        if choice == "create":
            file_name = input("Enter the name of the file to create: ")
            content = input("Enter the content of the file: ")
            base_folder = input("Enter the base folder name: ")
            target_folder = input("Enter the target folder name: ")
            create_document(file_name, content, base_folder, target_folder)

        elif choice == "edit":
            file_name = input("Enter the name of the file to edit: ")
            new_content = input("Enter the new content to append: ")
            base_folder = input("Enter the base folder name: ")
            target_folder = input("Enter the target folder name: ")
            edit_document(file_name, new_content, base_folder, target_folder)

        elif choice == "delete":
            file_name = input("Enter the name of the file to delete: ")
            base_folder = input("Enter the base folder name: ")
            target_folder = input("Enter the target folder name: ")
            delete_document(file_name, base_folder, target_folder)

        elif choice == "summarize":
            file_name = input("Enter the name of the file to summarize: ")
            base_folder = input("Enter the base folder name: ")
            target_folder = input("Enter the target folder name: ")
            print(summarize_document(file_name, base_folder, target_folder))

        elif choice == "classify":
            file_name = input("Enter the name of the file to classify: ")
            base_folder = input("Enter the base folder name: ")
            target_folder = input("Enter the target folder name: ")
            classify_document(file_name, base_folder, target_folder)

        elif choice == "move":
            file_name = input("Enter the name of the file to move: ")
            base_folder = input("Enter the base folder name: ")
            target_folder = input("Enter the target folder name: ")
            move_document(file_name, base_folder, target_folder)

        elif choice == "retrieve":
            base_folder = input("Enter the base folder name: ")
            target_folder = input("Enter the target folder name: ")
            document_name = input("Enter the name of the document to retrieve: ")
            retrieve_document(base_folder, target_folder, document_name)

        elif choice == "list":
            base_folder = input("Enter the base folder name: ")
            target_folder = input("Enter the target folder name: ")
            list_documents(base_folder, target_folder)

        elif choice == "exit":
            print("Exiting Document Management Module.")
            break

if __name__ == "__main__":
    main()
