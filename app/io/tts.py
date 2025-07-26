import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from ratelimit import limits, sleep_and_retry
import simpleaudio as sa

load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")

MAX_REQUESTS_PER_MINUTE = 1000
CHARACTER_QUOTA = 100_000

used_characters = 0

@sleep_and_retry
@limits(calls=MAX_REQUESTS_PER_MINUTE, period=60)
def call_murf_api(payload, headers):
    return requests.post("https://api.murf.ai/v1/speech/generate", json=payload, headers=headers)

def text_to_speech(text: str, voice_id: str = "en-US-natalie", autoplay: bool = True) -> Path:
    global used_characters

    text_length = len(text)
    if used_characters + text_length > CHARACTER_QUOTA:
        print(f"❌ Character limit exceeded: {used_characters + text_length} / {CHARACTER_QUOTA}")
        return None

    headers = {
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voiceId": voice_id,
        "style": "Promo"
    }

    response = call_murf_api(payload, headers)

    if response.status_code == 200:
        data = response.json()
        audio_url = data.get("audioFile")

        if not audio_url:
            print("⚠️ No audio URL returned.")
            return None

        used_characters += text_length
        print(f"📊 Character usage: {used_characters} / {CHARACTER_QUOTA}")

        audio_data = requests.get(audio_url)
        output_path = Path("response_audio.wav")
        with open(output_path, "wb") as f:
            f.write(audio_data.content)

        if autoplay:
            print("🔊 Playing audio...")
            wave_obj = sa.WaveObject.from_wave_file(str(output_path))
            play_obj = wave_obj.play()
            play_obj.wait_done()

        return output_path

    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None
