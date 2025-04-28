# utils/audio_utils.py
import sounddevice as sd
from scipy.io.wavfile import write
import os

# --- Audio settings ---
SAMPLE_RATE = 44100
DURATION = 5  # seconds
FILENAME = "user_input.wav"

def delete_file_safely(filepath):
    """
    Delete the file safely if it exists.
    """
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

def record_audio(filename, duration, sample_rate):
    """
    Record audio from the microphone and save it as a .wav file.
    """
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    write(filename, sample_rate, recording)
    return filename
