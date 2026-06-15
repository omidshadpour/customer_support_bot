from app.vector_store.chroma_db import get_vector_db
from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger("retrieval")

def retrieve_document(quesion: str , company_id: str):
    logger.info(f"Retrieving document dor company: { company_id}, question: '{quesion[:50]}'")
    vector_db = get_vector_db(company_id)

    try:
        results = vector_db.similarity_search(
            quesion,
            k = settings.RETRIEVAL_K
        )
        logger.debug(f"Found {len(results)} document")

        return results
    
    except Exception as e:
        logger.warning(f"Could not retrieve documents for company {company_id}: {str(e)}")
        return []
