import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# --- Groq client setup ---
client = Groq(api_key=api_key)

def generate_groq_response(context_messages: list, emotion: str) -> str:
    """
    Generate a response from Groq's LLM based on chat history and detected emotion.
    `context_messages` should be a list of dicts: [{"role": "user"/"assistant", "content": "..."}, ...]
    """
    # Insert a system prompt at the start of the chat for tone control
    system_prompt = {
        "role": "system",
        "content": f"You are a helpful and emotionally intelligent AI assistant. Respond with empathy and clarity. The user's current emotion is: {emotion}."
    }

    # Combine system prompt with the conversation history
    messages = [system_prompt] + context_messages

    # Make the API call to Groq
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
