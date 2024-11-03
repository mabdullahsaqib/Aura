import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firestore
cred = credentials.Certificate("../credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# Save or Append to Continuous Chat
def save_to_chat(session_id: str, command: str, response: str):
    """
    Append a new command-response pair to the continuous chat document.
    """
    chat_ref = db.collection("continuous_chats").document(session_id)

    # Data to append
    new_message = {
        "timestamp": datetime.now(),
        "command": command,
        "response": response
    }

    # Use Firestore's arrayUnion to append to the messages array
    chat_ref.set({"messages": firestore.ArrayUnion([new_message])}, merge=True)
    print(f"Appended to chat session {session_id}:", new_message)


# Retrieve Chat History
def retrieve_chat(session_id: str):
    """
    Retrieve the chat history for a given session.
    """
    chat_ref = db.collection("continuous_chats").document(session_id)
    chat = chat_ref.get()
    if chat.exists:
        print(f"Retrieved chat session {session_id}:")
        return chat.to_dict().get("messages", [])
    else:
        print(f"No chat found for session {session_id}.")
        return []


# Example Usage
if __name__ == "__main__":
    session_id = "session_001"  # Unique ID for a particular chat session

    # Append a new message to the chat
    save_to_chat(session_id, "From now on, your name will be jarvis", "Copy that!")
    # save_to_chat(session_id, "Tell me a joke.",
    #              "Why did the scarecrow win an award? Because he was outstanding in his field!")

    # Retrieve chat history
    chat_history = retrieve_chat(session_id)
    for message in chat_history:
        print(message)
