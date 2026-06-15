from fastapi import APIRouter, UploadFile , File, Form
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from app.services.rag import ask_question, ask_question_stream, extract_sources
from app.services.ingestion import process_pdf
from app.services.retrieval import retrieve_document
from app.services.analytics import get_analytics, init_db
from app.core.logger import get_logger
from app.core.config import settings
import asyncio
import os
import uuid


logger = get_logger("routes")
router = APIRouter()

init_db()

# ---- Admin Endpoints ----
@router.get("/")
def home():
    return {"message": "Customer Support Bot API Running"}

@router.post("/admin/upload")
async def upload_document(file: UploadFile = File(...), company_id: str = Form(...)):
    logger.info(f"Uploading document for company: {company_id}")
    os.makedirs(settings.UPLOAD_DIR , exist_ok=True)
    
    filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(settings.UPLOAD_DIR , filename)

    file_bytes = await file.read()
    with open(pdf_path , "wb") as f:
        f.write(file_bytes)
    
    logger.info(f"File saved: {pdf_path}")
    await asyncio.to_thread(process_pdf , pdf_path , company_id)
    logger.info(f"Document proccessed for company: {company_id}")

    return {
        "message": "Document uploaded  seccussfully",
        "company_id": company_id,
        "filename": file.filename
    }

@router.get("/admin/analytics/{company_id}")
async def get_company_analytics(company_id : str):
    logger.info(f"Getting analytics for company: {company_id}")
    analytics = get_analytics(company_id)
    return analytics


# ---- Customer Endpoints ----

class QuestionRequest(BaseModel):
    question: str
    company_id: str
    session_id: str


@router.post("/chat/ask")
async def ask(request: QuestionRequest):
    logger.info(f"Question for company: {request.company_id}")
    answer= ask_question(
        request.question,
        request.company_id,
        request.session_id
    )

    return answer

@router.post("/chat/ask-stream")
async def ask_stream(request: QuestionRequest):
    logger.info(f"Stream question for company: {request.company_id}")

    def generate():
        for token in ask_question_stream(
            request.question,
            request.company_id,
            request.session_id
        ):
            yield token

        
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/chat/sources")
async def get_sources(request: QuestionRequest):
    logger.info(f"Getting dources for company: {request.company_id}")

    docs = retrieve_document(request.question , request.company_id)
    sources = extract_sources(docs)

    return {"sources": sources}

@router.get("/widget/{company_id}" , response_class=HTMLResponse)
async def get_widget(company_id: str):
    logger.info(f"Widget requested for company: {company_id}")

    with open("app/ui/widget.html" , "r") as f:
        html = f.read()

    html = html.replace("{{COMPANY_ID}}", company_id)

    return html