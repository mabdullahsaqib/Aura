import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firestore
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Save to Memory
def save_to_memory(collection: str, data: dict):
    """
    Save a new memory document to the specified collection.
    """
    data['timestamp'] = datetime.now()  # add a timestamp
    db.collection(collection).add(data)
    print(f"Data saved to {collection} collection:", data)

# Retrieve Memory
def retrieve_memory(collection: str, limit: int = 10, order_by="timestamp"):
    """
    Retrieve recent memory documents from a collection.
    """
    memories = db.collection(collection).order_by(order_by, direction=firestore.Query.DESCENDING).limit(limit).stream()
    result = [memory.to_dict() for memory in memories]
    print(f"Retrieved {len(result)} memories from {collection}:")
    return result

# Update Memory
def update_memory(collection: str, doc_id: str, updates: dict):
    """
    Update a specific memory document by ID.
    """
    doc_ref = db.collection(collection).document(doc_id)
    doc_ref.update(updates)
    print(f"Updated document {doc_id} in {collection} with:", updates)

# Example Usage
if __name__ == "__main__":
    # Save a memory example
    save_to_memory("interaction_history", {"command": "From now on, your name will be Jarvis", "response": "Yes, Mr Stark, as you wish, I shall be known as Jarvis from now on", "context": "Assigning name"})

    # Retrieve recent memories
    memories = retrieve_memory("interaction_history", limit=5)
    print(memories)

    # # Update a memory example (replace 'your_doc_id' with actual document ID)
    # update_memory("interaction_history", "K2HAtSWXVCtRZWEtLXQG", {"context": "Updated weather inquiry"})
