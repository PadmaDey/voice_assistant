import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Must be at the top

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import uuid
from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
from transformers import pipeline, logging as hf_logging
from core.groq_response import generate_groq_response
from core.tts_engine import speak
from utils.audio_utils import record_audio, delete_file_safely
from core.huggingface_emotion import predict_emotion_hf
from utils.chroma_db import add_message, get_chat_history

# Suppress warning spam from HF pipeline
hf_logging.set_verbosity_error()

# Load environment
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Recording settings
DURATION = 5
SAMPLE_RATE = 44100
FILENAME = "user_input.wav"

# ASR pipeline
transcribe_pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    token=HF_TOKEN
)

# Format chat history for UI
def format_chat_history(raw_history):
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

# Home route
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

# Record trigger (via POST)
@app.route("/record", methods=["POST"])
def record_route():
    print("[INFO] Triggered recording route")
    delete_file_safely(FILENAME)
    session["status"] = "🎤 Listening..."
    return redirect(url_for("transcribe_route"))

# Transcription stage
@app.route("/transcribe", methods=["GET"])
def transcribe_route():
    try:
        print("[INFO] Starting audio recording...")
        session["status"] = "🎙️ Recording..."
        record_audio(FILENAME, DURATION, SAMPLE_RATE)

        print("[INFO] Transcribing with Whisper...")
        session["status"] = "🔍 Transcribing..."
        result = transcribe_pipe(FILENAME, return_timestamps=True)
        user_text = result["text"]
        print(f"[USER TEXT] {user_text}")

        session["user_text"] = user_text
        return redirect(url_for("emotion_route"))

    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        session["status"] = f"❌ Error during transcription: {str(e)}"
        return redirect(url_for("index"))

# Emotion detection stage
@app.route("/emotion", methods=["GET"])
def emotion_route():
    try:
        print("[INFO] Predicting emotion...")
        user_text = session.get("user_text")
        session["status"] = "😶 Detecting Emotion..."

        emotion, confidence = predict_emotion_hf(FILENAME, user_text)
        confidence_percent = round(confidence * 100)
        emotion_display = f"{emotion} ({confidence_percent}%)"
        print(f"[EMOTION] {emotion_display}")

        session["emotion"] = emotion
        session["emotion_display"] = emotion_display

        return redirect(url_for("generate_response_route"))

    except Exception as e:
        print(f"[ERROR] Emotion detection failed: {e}")
        session["status"] = f"❌ Error during emotion detection: {str(e)}"
        return redirect(url_for("index"))

# Response generation
@app.route("/generate", methods=["GET"])
def generate_response_route():
    try:
        print("[INFO] Generating LLM response...")
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

        add_message(session_id, "user", user_text, emotion=session["emotion_display"])
        add_message(session_id, "assistant", response)

        delete_file_safely(FILENAME)
        session["status"] = "✅ Complete!"
        return redirect(url_for("index"))

    except Exception as e:
        print(f"[ERROR] LLM response failed: {e}")
        session["status"] = f"❌ Error during response generation: {str(e)}"
        return redirect(url_for("index"))

# Fix for Method Not Allowed (405) — redirect on GET
@app.route("/record", methods=["GET"])
def record_redirect():
    print("[WARN] GET /record not allowed, redirecting...")
    return redirect(url_for("index"))

@app.route("/latest_chat", methods=["GET"])
def latest_chat():
    session_id = session.get("session_id")
    raw_history = get_chat_history(session_id)
    formatted = format_chat_history(raw_history)
    return {"chat_history": formatted[-1] if formatted else None}

# MAIN entry point (IMPORTANT for cloud / Docker deployments)
if __name__ == "__main__":
    print("🔧 Starting Voice Assistant Flask Server")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
