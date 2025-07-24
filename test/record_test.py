from app.transcribe import record_and_transcribe

if __name__ == "__main__":
    print("🧪 Starting live audio test...")
    query = record_and_transcribe()
    print("\n✅ Transcribed text:")
    print(query)
