
print("📥 Importing: embedding.py")
from functools import lru_cache
from sentence_transformers import SentenceTransformer
print("✅ Done importing: embedding.py")

@lru_cache()
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    model = get_embedding_model()
    return model.encode(text)
