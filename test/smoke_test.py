from app.transcribe import transcribe_audio
from app.summarizer import summarize_text
from app.chunker import chunk_text
from app.embedding import get_embedding
from app.vector_store import build_faiss_index, search_index

# Step 1: Transcription
transcript = transcribe_audio("data/sample_meeting.mp3")
print("\nTRANSCRIPT:\n")
print(transcript)

# Step 2: Summarization
summary = summarize_text(
    transcript + "Today we will work on the project called meet-assistent. Submit reports by tomorrow"
)
print("\nSUMMARY:\n")
print(summary)

# Step 3: Chunking
chunks = chunk_text(summary, max_tokens=10, overlap=2)
print("\nCHUNKS\n")
for chunk in chunks:
    print(chunk + '\n')

# Step 4: Embedding
print("\nEMBEDDINGS\n")
embeddings = []
for chunk in chunks:
    emb = get_embedding(chunk)
    embeddings.append(emb)
    print(emb)
    print("\n")

# Step 5: FAISS Index Build
index = build_faiss_index(embeddings)

# Step 6: Query
query_text = "what is the deadline of project?"
query_embedding = get_embedding(query_text)
top_indices = search_index(index, query_embedding, top_k=3)

print("\n🔍 TOP MATCHING CHUNKS:\n")
for i in top_indices:
    print(f"→ {chunks[i]}")
