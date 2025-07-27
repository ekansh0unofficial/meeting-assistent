import faiss
import numpy as np
from typing import List

def build_faiss_index(embeddings: List[List[float]]) -> faiss.IndexFlatL2:
    if not embeddings:
        raise ValueError("Embeddings list is empty.")
    
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype='float32'))
    return index

def search_index(index: faiss.IndexFlatL2, query_embedding: List[float], top_k: int = 3) -> List[int]:
    if not isinstance(index, faiss.Index):
        raise ValueError("Invalid FAISS index.")
    
    query = np.array([query_embedding], dtype='float32')
    distances, indices = index.search(query, top_k)
    return indices[0].tolist()
