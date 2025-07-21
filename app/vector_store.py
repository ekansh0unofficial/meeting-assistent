import faiss 
import numpy as np

def build_faiss_index(embeddings : list[list[float]]):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index

def search_index(index , query_embedding:list[float], top_k: int = 3):
    query = np.array([query_embedding]).astype('float32')
    distances ,indices = index.search(query , top_k)
    return indices[0]
