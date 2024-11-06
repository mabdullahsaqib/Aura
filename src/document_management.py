import os
from pathlib import Path
import google.generativeai as genai
from config import GEMINI_API_KEY

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def create_document(file_name, content):
    """
    Creates a new document with the specified content.

    Parameters:
        file_name (str): The name of the file to create.
        content (str): The content to write to the file.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Document '{file_name}' created successfully.")


def edit_document(file_name, new_content):
    """
    Edits an existing document by appending new content.

    Parameters:
        file_name (str): The name of the file to edit.
        new_content (str): The new content to append.
    """
    if Path(file_name).exists():
        with open(file_name, "a", encoding="utf-8") as file:
            file.write("\n" + new_content)
        print(f"Document '{file_name}' updated successfully.")
    else:
        print(f"Document '{file_name}' does not exist.")


def delete_document(file_name):
    """
    Deletes a document.

    Parameters:
        file_name (str): The name of the file to delete.
    """
    try:
        os.remove(file_name)
        print(f"Document '{file_name}' deleted successfully.")
    except FileNotFoundError:
        print(f"Document '{file_name}' not found.")


def summarize_document(file_name):
    """
    Summarizes the content of a document using Gemini.

    Parameters:
        file_name (str): The name of the file to summarize.

    Returns:
        str: The summary of the document.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()

        response = model.generate_content("Summarize the following file content: " + content )
        return response.text

    except FileNotFoundError:
        print(f"Document '{file_name}' not found.")
        return None


def retrieve_document(file_name):
    """
    Retrieves and displays the content of a document.

    Parameters:
        file_name (str): The name of the file to retrieve.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()
        print(f"\nContent of '{file_name}':\n{content}")
        return content
    except FileNotFoundError:
        print(f"Document '{file_name}' not found.")
        return None


def list_documents(directory="."):
    """
    Lists all documents in a specified directory.

    Parameters:
        directory (str): The directory to list documents from. Defaults to the current directory.

    Returns:
        list: A list of document file names.
    """
    doc_files = [f.name for f in Path(directory).iterdir() if f.is_file()]
    print("\nDocuments in directory:")
    for doc in doc_files:
        print(doc)
    return doc_files


def main():
    """
    Main function to interact with the Document Management Module.
    """
    print("Welcome to Aura's Document Management Module!")
    while True:
        choice = input("\nChoose an option: [create, edit, delete, summarize, retrieve, list, exit]: ").lower()

        if choice == 'create':
            file_name = input("Enter the document name: ")
            content = input("Enter the document content: ")
            create_document(file_name, content)

        elif choice == 'edit':
            file_name = input("Enter the document name: ")
            new_content = input("Enter the new content to add: ")
            edit_document(file_name, new_content)

        elif choice == 'delete':
            file_name = input("Enter the document name to delete: ")
            delete_document(file_name)

        elif choice == 'summarize':
            file_name = input("Enter the document name to summarize: ")
            summary = summarize_document(file_name)
            if summary:
                print("\nSummary:\n", summary)

        elif choice == 'retrieve':
            file_name = input("Enter the document name to retrieve: ")
            retrieve_document(file_name)

        elif choice == 'list':
            directory = input("Enter the directory to list documents from (leave blank for current directory): ") or "."
            list_documents(directory)

        elif choice == 'exit':
            print("Exiting the Document Management Module.")
            break


if __name__ == "__main__":
    main()
