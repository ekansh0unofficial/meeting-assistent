import whisper 
from pathlib import Path

def transcribe_audio(audio_path: str) -> str:
    print(f"loading audio : {audio_path}")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]