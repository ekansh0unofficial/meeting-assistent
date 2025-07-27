import whisper 
import sounddevice as sd
import os
import soundfile as sf
import numpy as np

model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    print(f"loading audio : {audio_path}")
    result = model.transcribe(audio_path)
    return result["text"]

def record_and_transcribe(output_path = "query.wav") -> str:
    fs = 44100
    recording = []
    sd.default.samplerate = fs
    sd.default.channels = 1

    def callback(indata, frames , time , status):
        recording.append(indata.copy())
    with sd.InputStream(callback=callback):
        input()
    audio_data = np.concatenate(recording , axis = 0)    
    sf.write(output_path , audio_data , fs)
    result = model.transcribe(output_path)  

    os.remove(output_path)
    return result["text"]  

