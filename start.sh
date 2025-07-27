apt-get update && apt-get install -y portaudio19-dev
python -m nltk.downloader stopwords punkt
uvicorn main:app --host 0.0.0.0 --port 10000
