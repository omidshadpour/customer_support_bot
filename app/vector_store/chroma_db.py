from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
from app.core.logger import get_logger
import chromadb

logger = get_logger("chroma_db")

embedding_model = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL,
    model_kwargs={"device":"cpu"},
    cache_folder = settings.MODELS_CACHE
) 

chromadb_client = chromadb.PersistentClient(path=settings.CHROMA_PATH)

def creat_vector_store(chunks , company_id: str):
    collection_name = f"{settings.COLLECTION_NAME}_{company_id}"
    logger.info(f"Storing {len(chunks)} chunks for company: {company_id}")

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        client=chromadb_client,
        collection_name=collection_name
    )

    logger.info(f"Chunks stored successfully for company: {company_id}")
    
    return vector_db

def get_vector_db(company_id: str):
    collection_name = f"{settings.COLLECTION_NAME}_{company_id}"

    return Chroma(
       client=chromadb_client,
       collection_name=collection_name,
       embedding_function=embedding_model
    )