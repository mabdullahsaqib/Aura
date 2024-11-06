import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
from datetime import datetime
from config import FIREBASE_CREDENTIALS_PATH , GEMINI_API_KEY

# Initialize Firestore
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def add_note(title, content, tags=None):
    """
    Adds a note to Firestore with a title, optional tags, and a timestamp.

    Parameters:
        title (str): The title of the note.
        content (str): The content of the note.
        tags (list of str): Optional tags for the note.
    """
    note_ref = db.collection("notes").document()
    note_data = {
        "note_id": note_ref.id,
        "title": title,
        "content": content,
        "timestamp": datetime.now(),
        "tags": tags if tags else []
    }
    note_ref.set(note_data)
    print("Note added successfully!")


def retrieve_notes(keyword=None, tag=None, date_range=None):
    """
    Retrieves notes based on a keyword, tag, or date range.

    Parameters:
        keyword (str): Keyword to search within note content.
        tag (str): Tag to filter notes.
        date_range (tuple of datetime): Start and end date for filtering notes.

    Returns:
        list: List of notes matching the criteria.
    """
    query = db.collection("notes")

    if tag:
        query = query.where("tags", "array_contains", tag)
    if date_range:
        start_date, end_date = date_range
        query = query.where("timestamp", ">=", start_date).where("timestamp", "<=", end_date)

    notes = [note.to_dict() for note in query.stream()]

    if keyword:
        notes = [note for note in notes if keyword.lower() in note["content"].lower()]

    return notes


def retrieve_all_notes():
    """
    Retrieves and displays all notes by their IDs and titles.

    Returns:
        list: A list of dictionaries containing note IDs and titles.
    """
    notes = db.collection("notes").stream()
    all_notes = [{"note_id": note.id, "title": note.to_dict().get("title", "Untitled")} for note in notes]

    print("\nAll Notes:")
    for note in all_notes:
        print(f"Note ID: {note['note_id']}, Title: {note['title']}")

    return all_notes


def summarize_note(note_content):
    """
    Summarizes a single note's content using Gemini.

    Parameters:
        note_content (str): The content of the note to summarize.

    Returns:
        str: Summary of the note.
    """
    response = model.generate_content("Summarize the following text: " + note_content)
    return response.text


def delete_note(note_id):
    """
    Deletes a note by note_id.

    Parameters:
        note_id (str): ID of the note to delete.
    """
    db.collection("notes").document(note_id).delete()
    print("Note deleted successfully!")


def edit_note(note_id, new_title=None, new_content=None, new_tags=None):
    """
    Edits a note's title, content, or tags.

    Parameters:
        note_id (str): ID of the note to edit.
        new_title (str): New title to replace the old title.
        new_content (str): New content to replace the old content.
        new_tags (list of str): New tags to replace the old tags.
    """
    note_ref = db.collection("notes").document(note_id)
    update_data = {}
    if new_title:
        update_data["title"] = new_title
    if new_content:
        update_data["content"] = new_content
    if new_tags is not None:
        update_data["tags"] = new_tags

    note_ref.update(update_data)
    print("Note updated successfully!")


def main():
    """
    Main function to interact with the Note-Taking Module.
    """
    print("Welcome to Aura's Note-Taking Module!")
    while True:
        choice = input("\nChoose an option: [add, retrieve, retrieve_all, summarize, delete, edit, exit]: ").lower()

        if choice == 'add':
            title = input("Enter the note title: ")
            content = input("Enter the note content: ")
            tags = input("Enter tags (comma-separated): ").split(",") if input(
                "Add tags? (y/n): ").lower() == 'y' else None
            add_note(title, content, tags)

        elif choice == 'retrieve':
            keyword = input("Enter a keyword to search (or leave blank): ") or None
            tag = input("Enter a tag to filter by (or leave blank): ") or None
            notes = retrieve_notes(keyword=keyword, tag=tag)
            for note in notes:
                print(f"\nNote ID: {note['note_id']}")
                print(f"Title: {note['title']}")
                print(f"Content: {note['content']}")
                print(f"Timestamp: {note['timestamp']}")
                print(f"Tags: {note.get('tags', [])}\n")

        elif choice == 'retrieve_all':
            retrieve_all_notes()

        elif choice == 'summarize':
            note_id = input("Enter the note ID to summarize: ")
            note = db.collection("notes").document(note_id).get()
            if note.exists:
                summary = summarize_note(note.to_dict()["content"])
                print("\nSummary:\n", summary)
            else:
                print("Note not found.")

        elif choice == 'delete':
            note_id = input("Enter the note ID to delete: ")
            delete_note(note_id)

        elif choice == 'edit':
            note_id = input("Enter the note ID to edit: ")
            new_title = input("Enter new title (leave blank to skip): ") or None
            new_content = input("Enter new content (leave blank to skip): ") or None
            new_tags = input("Enter new tags (comma-separated, or leave blank): ").split(",") if input(
                "Update tags? (y/n): ").lower() == 'y' else None
            edit_note(note_id, new_title, new_content, new_tags)

        elif choice == 'exit':
            print("Exiting the Note-Taking Module.")
            break


if __name__ == "__main__":
    main()
