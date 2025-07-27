from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.pipeline.query_pipeline import process_query
from app.io.tts import text_to_speech
from app.io.transcribe import transcribe_audio
from app.core.extractors import extract_context
import tempfile
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("timing")

router = APIRouter()
def safe_header(text: str, limit=200) -> str:
    return text.strip().replace("\n", " ")[:limit]


@router.post("/process/query")
async def process_audio_query(
    audio_file: UploadFile = File(...),
    context_file: UploadFile = File(None),
    context_text: str = Form(None)
):
    start = time.perf_counter()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(await audio_file.read())
        temp_audio_path = temp_audio.name
    log.info(f"📥 Audio saved in {time.perf_counter() - start:.2f}s")

    t1 = time.perf_counter()
    query_text = transcribe_audio(temp_audio_path)
    log.info(f"🗣️ Transcription took {time.perf_counter() - t1:.2f}s")

    t2 = time.perf_counter()
    if isinstance(context_file, str) or context_file is None:
        context_file = None
    if context_file:
        context_text = await extract_context(context_file)
    elif not context_text:
        return {"error": "Either context_text or context_file is required."}
    log.info(f"📄 Context extraction took {time.perf_counter() - t2:.2f}s")

    t3 = time.perf_counter()
    response = process_query(query_text, context_text)
    log.info(f"🧠 LLM response generation took {time.perf_counter() - t3:.2f}s")

    t4 = time.perf_counter()
    audio_path: Path = text_to_speech(response, autoplay=False)
    log.info(f"🔊 TTS took {time.perf_counter() - t4:.2f}s")

    total = time.perf_counter() - start
    log.info(f"✅ Total time for /process/query: {total:.2f}s")

    return FileResponse(
        path=audio_path,
        media_type="audio/wav",
        filename="response.wav",
        headers={
            "X-Query": safe_header(query_text),
            "X-Response": safe_header(response)
        }
)



@router.post("/process/text")
async def process_text_query(
    query_text: str = Form(...),
    context_file: UploadFile = File(None),
    context_text: str = Form(None)
):
    start = time.perf_counter()

    t1 = time.perf_counter()
    if isinstance(context_file, str) or context_file is None:
        context_file = None
    if context_file:
        context_text = await extract_context(context_file)
    elif not context_text:
        return {"error": "Either context_text or context_file is required."}
    log.info(f"📄 Context extraction took {time.perf_counter() - t1:.2f}s")

    t2 = time.perf_counter()
    response = process_query(query_text, context_text)
    log.info(f"🧠 LLM response generation took {time.perf_counter() - t2:.2f}s")

    t3 = time.perf_counter()
    audio_path: Path = text_to_speech(response, autoplay=False)
    log.info(f"🔊 TTS took {time.perf_counter() - t3:.2f}s")

    total = time.perf_counter() - start
    log.info(f"✅ Total time for /process/text: {total:.2f}s")

    return FileResponse(
        path=audio_path,
        media_type="audio/wav",
        filename="response.wav",
        headers={
            "X-Query": query_text,
            "X-Response": response
        }
    )
