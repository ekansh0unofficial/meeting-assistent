from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1" 
)

def ask_question(context: str, query: str) -> str:
    system_prompt = (
        "You are Jarvis, Ironman's intelligent AI assistant. "
        "Give helpful, multi-sentence responses with friendly tone."
    )

    user_prompt = f"Context:\n{context}\n\nQuestion:\n{query}"

    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
