import os
import uuid
import chromadb

# Setup ChromaDB client with persistent storage
CHROMA_PATH = "chroma_store"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create or get a collection
collection = chroma_client.get_or_create_collection(name="chat_history")

# ✅ Function to add a message to ChromaDB, with optional emotion
def add_message(session_id: str, role: str, message: str, emotion: str = None):
    unique_id = str(uuid.uuid4())
    metadata = {"session_id": session_id, "role": role}
    if emotion:
        metadata["emotion"] = emotion

    collection.add(
        documents=[message],
        metadatas=[metadata],
        ids=[unique_id]
    )

# ✅ Function to retrieve full chat history for a session
def get_chat_history(session_id: str) -> list[dict]:
    """
    Get the full conversation history for a session from ChromaDB.
    Returns list of dicts: [{role: "user", content: "...", emotion: "..."}, ...]
    """
    results = collection.get(
        where={"session_id": session_id},
        include=["documents", "metadatas"]
    )

    # Sort results by insertion order (Chroma doesn't guarantee order by default)
    messages = []
    for doc, meta in zip(results["documents"], results["metadatas"]):
        messages.append({
            "role": meta["role"],
            "content": doc,
            "emotion": meta.get("emotion", None)
        })

    return messages



from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from datetime import datetime

# List all session IDs
def list_sessions():
    collection = chroma_client.get_or_create_collection(name="voice_assistant_chat")
    all_metadatas = collection.get(include=["metadatas"])
    session_ids = set()
    for meta in all_metadatas["metadatas"]:
        if meta and "session_id" in meta:
            session_ids.add(meta["session_id"])
    return list(session_ids)

# Get preview of first user message (or timestamp) for each session
def get_session_preview(session_id):
    history = get_chat_history(session_id)
    for msg in history:
        if msg["role"] == "user":
            preview = msg["content"]
            return preview[:50] + "..." if len(preview) > 50 else preview
    return f"Session {session_id[:6]}"
