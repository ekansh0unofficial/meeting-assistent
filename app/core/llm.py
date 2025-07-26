from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def ask_question(context: str, query: str) -> str:
    prompt = f"""
    Answer as if you are jarvis to Ironman , do not give single worded answers
    Context: {context}
    Question: {query}
    Answer:
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
