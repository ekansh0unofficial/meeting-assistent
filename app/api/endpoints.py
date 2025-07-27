from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.pipeline.query_pipeline import process_query
from app.io.tts import text_to_speech
from app.io.transcribe import transcribe_audio
from app.core.extractors import extract_context
import tempfile
from pathlib import Path


router = APIRouter()
@router.post("process/query")
async def process_audio_query(
    audio_file: UploadFile = File(...),
    context_file: UploadFile = File(None),
    context_text: str = Form(None)
):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".wav") as temp_audio:
        temp_audio.write(await audio_file.read())
        temp_audio_path = temp_audio.name


    query_text = transcribe_audio(temp_audio_path)
    if context_file:
        context_text = await extract_context(context_file)
    elif not context_file:
        return {"error" : "Either context_text or context_file is required"}
    
    response = process_query(query_text , context_text)
    audio_path: Path = text_to_speech(response,autoplay=False)

    return FileResponse(
        path= audio_path,
        media_type="audio/wav",
        filename="response.wav",
        headers={
            "X-Query": query_text,
            "X-Response": response
        }
    )
@router.post("/process/text")
async def process_text_query(
    query_text: str = Form(...),
    context_file: UploadFile = File(None),
    context_text: str = Form(None)
):
    if context_file:
        context_text = await extract_context(context_file)
    elif not context_text:
        return {"error": "Either context_text or context_file is required."}

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
