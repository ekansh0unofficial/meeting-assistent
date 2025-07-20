from typing import List

def chunk_text(text: str , max_tokens:int = 200 , overlap: int =50)-> List[str]:
    words = text.split()
    chunks = []

    start = 0 
    while start < len(words):
        end = min(start + max_tokens , len(words))
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start+=max_tokens -overlap
    return chunks    