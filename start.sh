python -m nltk.downloader stopwords punkt
uvicorn main:app --host 0.0.0.0 --port 10000
