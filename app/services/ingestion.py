from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.vector_store.chroma_db import creat_vector_store
from app.core.exceptions import PDFProcessingError , VectorStoreError
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("ingestion")

def load_pdf(pdf_path: str):

    try:
        logger.info(f"Loading PDF: {pdf_path}")
        
        loader = PyPDFLoader(pdf_path)
        document = loader.load()

        logger.info(f"PDF loaded seccussfully: {len(document)} pages")

        return document
    
    except Exception as e:
        logger.error(f"Failed to load PDF: {str(e)}")
        raise PDFProcessingError(str(e))


def creat_chunks(document):
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP 
    ).split_documents(document)

    logger.debug(f"Creat {len(chunks)} chunks")

    return chunks

def process_pdf(pdf_path: str, company_id: str):

    try:
        logger.info(f"Processing PDF for company: {company_id}")

        document = load_pdf(pdf_path)
        chunks = creat_chunks(document)

        for chunk in chunks:
            chunk.metadata["company_id"] = company_id
            chunk.metadata["sources"] = pdf_path

        creat_vector_store(chunks , company_id)

        logger.info(f"PDF processed succussfully for company: {company_id}")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise VectorStoreError(str(e))
