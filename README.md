# Project Prompt GPT - Voice Bot Learning Project

## Developer Background & Goals

The developer is originally a **Flutter mobile developer** who began exploring AI and ML concepts via **LangChain**. Upon discovering the **Murf AI Coding Challenge**, the following goals were set:

1. **Participate in the Murf AI TTS Coding Contest** using free credits
2. **Learn LangChain** from both theoretical and applied perspectives
3. **Build a Flutter project** that showcases integration of voice + AI features

> This project forms a bridge between Flutter front-end skills and new backend/ML capabilities.

---

## Key Objectives

This project is intended purely for **learning purposes** and represents a **basic practical application** in the AI domain. The developer aims to achieve the following goals:

1. **Learn how to navigate an AI-related project**
2. **Understand and implement LangChain (both theory and application)**
3. **Integrate Murf AI API for Text-to-Speech (TTS)**


---

## Project Description

This project can best be described as a **Voice Bot**. Its functionality is divided into the following stages:

1. **Input Context**: Accepts input in the form of a **Text File** (`.pdf`, `.docx`, `.txt`) or an **Audio File** (`.wav`, `.mp3`) to provide the **context** for conversation.
2. **Audio Query Input**: Takes a **live audio stream** from the user and converts it into text.
3. **LLM Response**: Uses the provided context and query to generate a response via a Language Model.
4. **Audio Output**: Converts the LLM-generated response into audio using the **Murf AI TTS API** and serves it to the user.

---

## Current Refactored Structure (as of July 2025)

Project has been modularized for clarity and future integration (e.g., with Flutter or REST API).

```plaintext
voice-bot/
👉️ app/
👉️ 📁 core/                  # Logic Modules
👉️ ├── summarizer.py
👉️ ├── chunker.py
👉️ ├── embedding.py
👉️ ├── vector_store.py
👉️ ├── llm.py
👉️ └── extractors.py
👉️ 📁 io/                    # Input/Output Interfaces
👉️ ├── transcribe.py      # Audio input (file + mic)
👉️ └── tts.py             # MurfAI text-to-speech with playback & rate limit
👉️ 📁 pipeline/
👉️ └── query_pipeline.py  # Full processing pipeline
👉️ 📁 api/                   # FastAPI REST endpoints
👉️ └── endpoints.py
👉️ main.py                    # FastAPI app entry point
👉️ test/
👉️ ├── record_test.py
👉️ ├── smoke_test.py
👉️ ├── voice_query_test.py
👉️ └── tts_test.py
👉️ data/
👉️ └── sample_meeting.mp3
```

---

## Core Modules

### 1. `io/transcribe.py`

- **Tool**: OpenAI Whisper + SoundDevice + SoundFile
- **Functions**:
  - `transcribe_audio(path)` — For static `.wav`/`.mp3` file input
  - `record_and_transcribe_until_keypress()` — Records mic input until user presses ENTER
- **Optimizations**:
  - Lazy-loading of Whisper model using `get_whisper_model()` to reduce cold-start time
  - Replaced Whisper with `faster-whisper` for significantly lower latency
  - Removed redundant imports and handling logic from older Whisper implementation

### 2. `core/summarizer.py`

- **Tool**: NLTK
- **Function**: Summarizes input text using word frequencies
- **Optimizations**:
  - Efficient word frequency and sentence scoring using comprehensions
  - Stopword filtering and alpha-only word checks done in a single pass
  - Uses `sum()` for cleaner sentence scoring

### 3. `core/chunker.py`

- **Function**: Splits summarized text into overlapping word-based chunks
- **Optimizations**:
  - Supports adjustable chunk size and overlap for flexibility
  - Clean logic using `start += max_tokens - overlap`

### 4. `core/embedding.py`

- **Tool**: SentenceTransformer (`all-MiniLM-L6-v2`)
- **Function**: Converts each chunk and query into semantic vector embeddings
- **Optimizations**:
  - Lazy-loaded model using `@lru_cache()` to avoid reloading
  - Supports both single string and list input for batch embeddings
  - Clean typing and `show_progress_bar=False` for fast CLI output

### 5. `core/vector_store.py`

- **Tool**: FAISS
- **Functions**:
  - `build_faiss_index()` — Builds similarity search index from a list of float vectors
  - `search_index()` — Finds top matching chunks
- **Optimizations**:
  - Type-safe and API-friendly (returns pure Python list)
  - Includes validation for empty data or invalid index inputs

### 6. `core/llm.py`

- **Model**: `Qwen3-Coder-480B` via **Together.ai API** (Open-source, API-based, free)
- **Function**: Answers a question using a prompt with top chunks as context
- **Optimizations**:
  - Switched from local `flan-t5-base` model to free, faster Together API
  - Uses prompt formatting for Jarvis-style responses

### 7. `pipeline/query_pipeline.py`

- **Function**: `process_query_pipeline(query_text, context_text)`
- **Purpose**: Runs entire chain:
  - summarization → chunking → embedding → retrieval → response generation

### 8. `io/tts.py`

- **Tool**: Murf AI API + `simpleaudio` for playback
- **Function**: `text_to_speech()` converts LLM response into speech
- **Features**:
  - Automatically downloads and plays voice
  - Tracks character usage from 100k limit
  - Rate-limited to 1000 requests/minute using `ratelimit`

---

## 🧠 Auditory Query Input Logic

### Function: `record_and_transcribe_until_keypress()`

- Uses `sounddevice` to continuously record mic input
- Press ENTER to stop recording
- Saves as `.wav`, transcribes using **faster-whisper**
- Returns clean text string as query

**Benefits:**

- No fixed duration; user can speak freely
- Accurate transcription using optimized Whisper variant
- Lazy-loading prevents redundant reloads
- Cleanly integrated into test and pipeline flow

---

## 🧪 Pipeline Usage Example

```python
from app.io.transcribe import record_and_transcribe_until_keypress
from app.pipeline.query_pipeline import process_query_pipeline

context_text = """Paste a long text or transcript here."""
query_text = record_and_transcribe_until_keypress()
response = process_query_pipeline(query_text, context_text)
print("\n🤖 Response:\n", response)
```

---

## 🔊 TTS API Rate Limit Handling

- ✅ 100k character limit tracked via `used_characters`
- ✅ 1000 requests/min limited using `@limits` from `ratelimit`
- ✅ Only plays audio if `autoplay=True`
- ❗ In-memory counters (can be persisted in future)

---

## ✅ REST API Setup

Using **FastAPI**, we created a lightweight REST API backend:

### Routes

- `POST /process/query`

  - Accepts: `audio_file` + `context_text`
  - Tracks performance with `time.perf_counter()` and `logging`
  - Returns: JSON response and plays audio

- `POST /process/text`

  - Accepts: `query_text` + `context_text`
  - Processes query → LLM → TTS
  - Returns: JSON response and plays audio

- `GET /ping`

  - Health check endpoint

### Entry Point

```python
# main.py
from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="Voice Bot Api",
    description="REST API for audio-based AI query bot",
    version="0.1"
)

app.include_router(router)

@app.get("/ping")
async def ping():
    return {"message": "api is live"}
```

Run using:

```bash
uvicorn app.main:app --reload
```

---

## Gaps and Uncertainties

- ✅ Together AI integration complete using free open-source models
- ✅ Murf AI TTS is fully integrated and working
- ✅ REST API layer implemented with FastAPI
- ✅ Whisper replaced by `faster-whisper`
- ❌ Still pending: Flutter integration (frontend)
- ❌ LangChain integration roadmap TBD

---

## ✅ Completed Steps So Far

- ☑️ Modularized codebase into `app/` structure
- ☑️ Whisper replaced by faster-whisper
- ☑️ Together.ai used as external LLM (free API)
- ☑️ Murf AI integration with request limits and audio playback
- ☑️ REST API implemented with FastAPI
- ☑️ Timestamped logging added to all critical stages

---

**End of Document**

