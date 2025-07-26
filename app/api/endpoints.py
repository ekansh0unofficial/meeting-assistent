from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.pipeline.query_pipeline import process_query
from app.io.tts import text_to_speech
from app.io.transcribe import transcribe_audio
import tempfile
from pathlib import Path

router = APIRouter()

@router.post("/process/query")
async def process_audio_query(
    context_text: str = Form(...),
    audio_file: UploadFile = File(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(await audio_file.read())
        temp_path = temp_audio.name

    query_text = transcribe_audio(temp_path)

    response = process_query(query_text, context_text)

    audio_path: Path = text_to_speech(response, autoplay=False)

    return FileResponse(
        path=audio_path,
        media_type="audio/wav",
        filename="response.wav",
        headers={
            "X-Query": query_text,
            "X-Response": response
        }
    )


@router.post("/process/text")
async def process_text_query(
    context_text: str = Form(...),
    query_text: str = Form(...)
):
    response = process_query(query_text, context_text)

    audio_path: Path = text_to_speech(response, autoplay=False)

    return FileResponse(
        path=audio_path,
        media_type="audio/wav",
        filename="response.wav",
        headers={
            "X-Query": query_text,
            "X-Response": response
        }
    )
