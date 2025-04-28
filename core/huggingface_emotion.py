from transformers import pipeline
import warnings
from transformers.utils import logging as hf_logging

# Suppress warnings
warnings.filterwarnings("ignore")
hf_logging.set_verbosity_error()

# Load speech-based emotion pipeline
speech_emotion_classifier = pipeline(
    "audio-classification",
    model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
    top_k=1
)

# Load text-based emotion pipeline (this one understands context well)
text_emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True,
    top_k=1
)

def predict_emotion_from_text(text):
    """
    Predict emotion using text-based emotion classification model.
    Returns: (emotion, confidence)
    """
    results = text_emotion_classifier(text)
    if results and results[0]:
        best = results[0][0]
        return best['label'].lower(), best['score']
    return "neutral", 0.5

def predict_emotion_hf(audio_path=None, user_text=None):
    """
    Predict emotion from speech and/or text, and return the more confident result.
    """
    audio_emotion, audio_conf = None, 0.0
    text_emotion, text_conf = None, 0.0

    if audio_path:
        try:
            result = speech_emotion_classifier(audio_path)
            if result:
                audio_emotion = result[0]['label'].lower()
                audio_conf = result[0]['score']
        except Exception as e:
            print("Audio emotion error:", str(e))

    if user_text:
        try:
            text_emotion, text_conf = predict_emotion_from_text(user_text)
        except Exception as e:
            print("Text emotion error:", str(e))

    # 🔀 Choose the one with higher confidence
    if text_conf >= audio_conf:
        return text_emotion, text_conf
    else:
        return audio_emotion, audio_conf
