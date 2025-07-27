from PyPDF2 import PdfReader
import docx
from app.io.transcribe import transcribe_audio
import tempfile

async def extract_context(uploaded_file):
    filename = uploaded_file.filename
    suffix = filename.split('.')[-1].lower()

    contents = await uploaded_file.read()
    if(suffix == "txt" or suffix == "mid"):
        return contents.decode("utf-8")
    elif suffix == "pdf":
        with tempfile.NamedTemporaryFile(delete=False , suffix=".pdf") as tmp:
            tmp.write(contents)
            reader = PdfReader(tmp.name)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text
    elif suffix == "docx":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(contents)
            doc = docx.Document(tmp.name)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs) 
    elif suffix in ("mp3" , "wav"):
        with tempfile.NamedTemporaryFile(delete=False , suffix=f".{suffix}") as tmp:
            tmp.write(contents)
            return transcribe_audio(tmp.name)
    else:
        return "Unsupported File Type"
            