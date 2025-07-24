# test/test_voice_query_to_llm.py

from app.transcribe import record_and_transcribe
from app.chunker import chunk_text
from app.embedding import get_embedding
from app.vector_store import build_faiss_index, search_index
from app.llm import ask_question
from app.summarizer import summarize_text

# STEP 0: Provide input context (could come from a file later)
context_text = """
Your large transcript or summarized meeting notes or PDF content would go here.
For testing, just paste a paragraph or two.
"""

# STEP 1: Preprocess context (summarize → chunk → embed → build index)
summary = summarize_text(context_text)
chunks = chunk_text(summary)
embeddings = [get_embedding(chunk) for chunk in chunks]
faiss_index = build_faiss_index(embeddings)

# STEP 2: Get voice query from mic
print('Speak Now')
query_text = record_and_transcribe()
print("\n🎤 You asked:", query_text)

# STEP 3: Embed the query
query_embedding = get_embedding(query_text)

# STEP 4: Retrieve top relevant chunks
top_indices = search_index(faiss_index, query_embedding, top_k=3)
top_chunks = [chunks[i] for i in top_indices]

# STEP 5: Join chunks as context
retrieved_context = "\n".join(top_chunks)

# STEP 6: Ask the LLM
answer = ask_question(retrieved_context, query_text)
print("\n🧠 Response from LLM:\n", answer)
