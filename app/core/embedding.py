from functools import lru_cache
from sentence_transformers import SentenceTransformer
from typing import Union, List

@lru_cache()
def get_embedding_model() -> SentenceTransformer:
    print("🔄 Loading SentenceTransformer model: all-MiniLM-L6-v2")
    return SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
    model = get_embedding_model()
    return model.encode(text, show_progress_bar=False)
