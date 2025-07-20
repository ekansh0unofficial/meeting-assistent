from app.transcribe import transcribe_audio
from app.summarizer import summarize_text
from app.chunker import chunk_text

transcript = transcribe_audio("data/sample_meeting.mp3")
print("\nTRANSCRIPT:\n")
print(transcript)

summary = summarize_text(
    transcript + "Today we will work on the project called meet-assistent. Submit reports by tomorrow"
)

print("\nSUMMARY:\n")
print(summary)

chunks = chunk_text(summary , max_tokens=10 , overlap=2)
print("\nCHUNKS\n")
for chunk in chunks:
    print(chunk + '\n')