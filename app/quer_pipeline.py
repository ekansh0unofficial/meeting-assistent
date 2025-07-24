from app.summarizer import summarize_text
from app.chunker import chunk_text
from app.embedding import get_embedding
from app.vector_store import build_faiss_index , search_index
from app.llm import ask_question

def process_query(query:str , context : str , top_k: int = 3) -> str:
    summary = summarize_text(context)

    chunks = chunk_text(summary)

    embeddings = [get_embedding(chunk) for chunk in chunks]

    faiss_index = build_faiss_index()

    query_embedding = get_embedding(query)

    top_indices = search_index(faiss_index , query_embedding , top_k)
    
    top_chunks = [chunks[i] for i in top_indices]
    
    retrieved_context = '\n'.join(top_chunks)
    
    response = ask_question(retrieved_context , query)
    
    return response


