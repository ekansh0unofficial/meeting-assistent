# test/test_voice_query_to_llm.py

from app.io.transcribe import record_and_transcribe
from app.pipeline.query_pipeline import process_query
from app.io.tts import text_to_speech

context_text = """
Machine learning (ML) is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and generalise to unseen data, and thus perform tasks without explicit instructions.[1] Within a subdiscipline in machine learning, advances in the field of deep learning have allowed neural networks, a class of statistical algorithms, to surpass many previous machine learning approaches in performance
ML finds application in many fields, including natural language processing, computer vision, speech recognition, email filtering, agriculture, and medicine.[3][4] The application of ML to business problems is known as predictive analytics."""
print('Speak Now')
query_text = record_and_transcribe()
answer = process_query(query_text , context_text)
print("\n🎤 You asked:", query_text)
print(answer)
text_to_speech(answer)
