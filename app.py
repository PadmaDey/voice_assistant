import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Must be at the top

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import uuid
import warnings
from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
from transformers import pipeline, logging as hf_logging

from core.groq_response import generate_groq_response
from core.tts_engine import speak
from core.huggingface_emotion import predict_emotion_hf
from utils.audio_utils import record_audio, delete_file_safely
from utils.chroma_db import add_message, get_chat_history

# Suppress logging from third-party libraries
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
warnings.filterwarnings("ignore", category=DeprecationWarning)
hf_logging.set_verbosity_error()

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Audio and model config
DURATION = 5
SAMPLE_RATE = 44100
FILENAME = "user_input.wav"

transcribe_pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    token=HF_TOKEN
)

def format_chat_history(raw_history):
    """Format raw DB chat entries for UI display."""
    formatted = []
    current_user_msg = None
    current_emotion = None
    for entry in raw_history:
        if entry["role"] == "user":
            current_user_msg = entry["content"]
            current_emotion = entry.get("emotion", "🤖")
        elif entry["role"] == "assistant" and current_user_msg:
            formatted.append({
                "user": current_user_msg,
                "emotion": current_emotion,
                "response": entry["content"]
            })
            current_user_msg = None
            current_emotion = None
    return formatted

@app.route("/", methods=["GET", "POST"])
def index():
    session_id = session.get("session_id", str(uuid.uuid4()))
    session["session_id"] = session_id
    print(f"[INFO] Session ID: {session_id}")

    raw_history = get_chat_history(session_id)
    chat_history = format_chat_history(raw_history)
    status = session.get("status", "🎤 Ready to Listen")

    return render_template("index.html", chat_history=chat_history,
                           status=status, session_id=session_id)

@app.route("/record", methods=["POST"])
def record_route():
    print("[INFO] Triggered recording route")
    delete_file_safely(FILENAME)
    session["status"] = "🎤 Listening..."
    return redirect(url_for("transcribe_route"))

@app.route("/transcribe", methods=["GET"])
def transcribe_route():
    try:
        print("[INFO] Recording audio...")
        session["status"] = "🎙️ Recording..."
        record_audio(FILENAME, DURATION, SAMPLE_RATE)

        print("[INFO] Transcribing with Whisper...")
        session["status"] = "🔍 Transcribing..."
        result = transcribe_pipe(FILENAME, return_timestamps=True)
        user_text = result["text"].strip()
        print(f"[USER TEXT] {user_text}")

        session["user_text"] = user_text
        return redirect(url_for("emotion_route"))

    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        session["status"] = f"❌ Transcription error: {str(e)}"
        return redirect(url_for("index"))

@app.route("/emotion", methods=["GET"])
def emotion_route():
    try:
        print("[INFO] Predicting emotion...")
        user_text = session.get("user_text")
        session["status"] = "😶 Detecting Emotion..."

        emotion, confidence = predict_emotion_hf(FILENAME, user_text)
        display = f"{emotion} ({round(confidence * 100)}%)"
        print(f"[EMOTION] {display}")

        session["emotion"] = emotion
        session["emotion_display"] = display

        return redirect(url_for("generate_response_route"))

    except Exception as e:
        print(f"[ERROR] Emotion detection failed: {e}")
        session["status"] = f"❌ Emotion detection error: {str(e)}"
        return redirect(url_for("index"))

@app.route("/generate", methods=["GET"])
def generate_response_route():
    try:
        print("[INFO] Generating response...")
        session_id = session["session_id"]
        raw_history = get_chat_history(session_id)
        context = [{"role": msg["role"], "content": msg["content"]} for msg in raw_history]

        user_text = session["user_text"]
        emotion = session.get("emotion")

        context.append({"role": "user", "content": user_text})
        session["status"] = "💬 Generating Response..."

        response = generate_groq_response(context, emotion)
        print(f"[BOT RESPONSE] {response}")
        session["response"] = response

        speak(response, emotion)

        # Persist to DB
        add_message(session_id, "user", user_text, emotion=session["emotion_display"])
        add_message(session_id, "assistant", response)

        delete_file_safely(FILENAME)
        session["status"] = "✅ Complete!"
        return redirect(url_for("index"))

    except Exception as e:
        print(f"[ERROR] LLM response failed: {e}")
        session["status"] = f"❌ LLM error: {str(e)}"
        return redirect(url_for("index"))

@app.route("/record", methods=["GET"])
def record_redirect():
    print("[WARN] GET /record not allowed, redirecting to index.")
    return redirect(url_for("index"))

@app.route("/latest_chat", methods=["GET"])
def latest_chat():
    session_id = session.get("session_id")
    raw_history = get_chat_history(session_id)
    formatted = format_chat_history(raw_history)
    return {"chat_history": formatted[-1] if formatted else None}

if __name__ == "__main__":
    print("🔧 Starting Voice Assistant Flask Server")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
