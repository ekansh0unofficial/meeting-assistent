import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
from typing import Optional

# Load Whisper model once globally
_model = None

def get_whisper_model(name: str = "base"):
    global _model
    if _model is None:
        print(f"🔄 Loading Whisper model: {name}")
        _model = whisper.load_model(name)
    return _model

def transcribe_audio(audio_path: str) -> str:
    model = get_whisper_model()
    print(f"🎧 Transcribing audio file: {audio_path}")
    result = model.transcribe(audio_path)
    return result["text"]

def record_and_transcribe(output_path: str = "query.wav") -> str:
    fs = 44100
    sd.default.samplerate = fs
    sd.default.channels = 1

    recording = []

    def callback(indata, frames, time, status):
        if status:
            print(f"⚠️ Recording status: {status}")
        recording.append(indata.copy())

    print("🎙️ Speak into your mic. Press ENTER to stop recording...")
    with sd.InputStream(callback=callback):
        input()  # Wait for user to press Enter

    audio_data = np.concatenate(recording, axis=0)
    sf.write(output_path, audio_data, fs)

    model = get_whisper_model()
    result = model.transcribe(output_path)

    # Cleanup temp file
    try:
        os.remove(output_path)
    except OSError:
        print(f"❌ Could not delete temporary file: {output_path}")

    return result["text"]
