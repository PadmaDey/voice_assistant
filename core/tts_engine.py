# core/tts_engine.py
import pyttsx3

def speak(text, emotion):
    """
    Convert text to speech with a rate adjusted for the detected emotion.
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice = voices[1].id if len(voices) > 1 else voices[0].id
    rate = 150  # default rate

    if emotion.lower() == "happy":
        rate = 190
    elif emotion.lower() == "sad":
        rate = 140
    elif emotion.lower() == "angry":
        rate = 175
    elif emotion.lower() == "surprised":
        rate = 200
    elif emotion.lower() == "neutral":
        rate = 160

    engine.setProperty("voice", voice)
    engine.setProperty("rate", rate)

    engine.say(text)
    engine.runAndWait()
