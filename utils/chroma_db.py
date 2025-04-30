# import os
# import uuid
# import chromadb

# # Setup ChromaDB client with persistent storage
# CHROMA_PATH = "chroma_store"
# chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# # Create or get a collection
# collection = chroma_client.get_or_create_collection(name="chat_history")

# # ✅ Function to add a message to ChromaDB, with optional emotion
# def add_message(session_id: str, role: str, message: str, emotion: str = None):
#     unique_id = str(uuid.uuid4())
#     metadata = {"session_id": session_id, "role": role}
#     if emotion:
#         metadata["emotion"] = emotion

#     collection.add(
#         documents=[message],
#         metadatas=[metadata],
#         ids=[unique_id]
#     )

# # ✅ Function to retrieve full chat history for a session
# def get_chat_history(session_id: str) -> list[dict]:
#     """
#     Get the full conversation history for a session from ChromaDB.
#     Returns list of dicts: [{role: "user", content: "...", emotion: "..."}, ...]
#     """
#     results = collection.get(
#         where={"session_id": session_id},
#         include=["documents", "metadatas"]
#     )

#     # Sort results by insertion order (Chroma doesn't guarantee order by default)
#     messages = []
#     for doc, meta in zip(results["documents"], results["metadatas"]):
#         messages.append({
#             "role": meta["role"],
#             "content": doc,
#             "emotion": meta.get("emotion", None)
#         })

#     return messages



# from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
# from datetime import datetime

# # List all session IDs
# def list_sessions():
#     collection = chroma_client.get_or_create_collection(name="voice_assistant_chat")
#     all_metadatas = collection.get(include=["metadatas"])
#     session_ids = set()
#     for meta in all_metadatas["metadatas"]:
#         if meta and "session_id" in meta:
#             session_ids.add(meta["session_id"])
#     return list(session_ids)

# # Get preview of first user message (or timestamp) for each session
# def get_session_preview(session_id):
#     history = get_chat_history(session_id)
#     for msg in history:
#         if msg["role"] == "user":
#             preview = msg["content"]
#             return preview[:50] + "..." if len(preview) > 50 else preview
#     return f"Session {session_id[:6]}"









# import os
# import uuid
# from datetime import datetime
# import chromadb
# from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# # Setup ChromaDB client with persistent storage
# CHROMA_PATH = "chroma_store"
# chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# # Create or get the main collection
# collection = chroma_client.get_or_create_collection(name="chat_history")

# # ✅ Function to add a message to ChromaDB
# def add_message(session_id: str, role: str, message: str, emotion: str = None):
#     """
#     Add a message to ChromaDB with optional emotion metadata.
#     """
#     unique_id = str(uuid.uuid4())
#     metadata = {"session_id": session_id, "role": role}
#     if emotion:
#         metadata["emotion"] = emotion

#     collection.add(
#         documents=[message],
#         metadatas=[metadata],
#         ids=[unique_id]
#     )

# # ✅ Function to retrieve full chat history for a session
# def get_chat_history(session_id: str) -> list[dict]:
#     """
#     Get the full conversation history for a session from ChromaDB.
#     Returns list of dicts: [{role: "user", content: "...", emotion: "..."}, ...]
#     """
#     if not session_id or not isinstance(session_id, str):
#         raise ValueError("Invalid session_id provided to get_chat_history()")

#     results = collection.get(
#         where={"session_id": session_id},
#         include=["documents", "metadatas"]
#     )

#     messages = []
#     for doc, meta in zip(results["documents"], results["metadatas"]):
#         messages.append({
#             "role": meta["role"],
#             "content": doc,
#             "emotion": meta.get("emotion", None)
#         })

#     return messages

# # ✅ List all unique session IDs
# def list_sessions() -> list[str]:
#     """
#     Return a list of all unique session IDs found in the 'voice_assistant_chat' collection.
#     """
#     session_collection = chroma_client.get_or_create_collection(name="voice_assistant_chat")
#     all_metadatas = session_collection.get(include=["metadatas"])
#     session_ids = {
#         meta["session_id"] for meta in all_metadatas["metadatas"]
#         if meta and "session_id" in meta
#     }
#     return list(session_ids)

# # ✅ Get a preview of the first user message in a session
# def get_session_preview(session_id: str) -> str:
#     """
#     Return a short preview (first 50 chars) of the user's first message in a session.
#     """
#     history = get_chat_history(session_id)
#     for msg in history:
#         if msg["role"] == "user":
#             preview = msg["content"]
#             return preview[:50] + "..." if len(preview) > 50 else preview
#     return f"Session {session_id[:6]}"








import os
import uuid
from typing import Optional, List, Dict
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# ========================== Setup ==========================

CHROMA_PATH = "chroma_store"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Main collection for chat history
CHAT_COLLECTION_NAME = "chat_history"
chat_collection = chroma_client.get_or_create_collection(name=CHAT_COLLECTION_NAME)

# ========================== Core Functions ==========================

def add_message(session_id: str, role: str, message: str, emotion: Optional[str] = None) -> None:
    """
    Store a message in ChromaDB with optional emotion metadata.

    Args:
        session_id (str): Unique ID representing the chat session.
        role (str): Either "user" or "assistant".
        message (str): The message text.
        emotion (str, optional): Detected emotion for user input.
    """
    unique_id = str(uuid.uuid4())
    metadata = {"session_id": session_id, "role": role}
    if emotion:
        metadata["emotion"] = emotion

    chat_collection.add(
        documents=[message],
        metadatas=[metadata],
        ids=[unique_id]
    )

def get_chat_history(session_id: str) -> List[Dict[str, Optional[str]]]:
    """
    Retrieve the entire chat history for a session.

    Args:
        session_id (str): The session identifier.

    Returns:
        List[Dict]: List of messages with role, content, and emotion (if available).
    """
    if not session_id or not isinstance(session_id, str):
        raise ValueError("Invalid session_id provided to get_chat_history().")

    results = chat_collection.get(
        where={"session_id": session_id},
        include=["documents", "metadatas"]
    )

    return [
        {
            "role": meta["role"],
            "content": doc,
            "emotion": meta.get("emotion")
        }
        for doc, meta in zip(results["documents"], results["metadatas"])
    ]

# ========================== Session Utilities ==========================

def list_sessions() -> List[str]:
    """
    List all unique session IDs from a dedicated collection.

    Returns:
        List[str]: A list of unique session identifiers.
    """
    session_collection = chroma_client.get_or_create_collection(name="voice_assistant_chat")
    results = session_collection.get(include=["metadatas"])

    session_ids = {
        meta["session_id"]
        for meta in results["metadatas"]
        if meta and "session_id" in meta
    }

    return list(session_ids)

def get_session_preview(session_id: str) -> str:
    """
    Get a short preview of the first user message in a session.

    Args:
        session_id (str): The session identifier.

    Returns:
        str: A shortened preview of the user's first message, or fallback ID.
    """
    history = get_chat_history(session_id)
    for msg in history:
        if msg["role"] == "user":
            preview = msg["content"]
            return preview[:50] + "..." if len(preview) > 50 else preview
    return f"Session {session_id[:6]}"
