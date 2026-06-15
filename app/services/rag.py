from app.services.retrieval import retrieve_document
from app.llm.groq_service import generate_answer , generate_answer_stream
from app.core.exceptions import CompanyNotFoundError , LLMError
from app.core.logger import get_logger
from app.services.memory import get_history , add_message
from app.services.analytics import save_question
from typing import Generator

logger = get_logger("rag")

def build_content(retrieve_docs):
    context = ""
    for doc in retrieve_docs:
        context += doc.page_content + "\n\n"
    return context

def creat_prompt(question , context , history):
    history_text = ""
    for msg in history:
        history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are a helpful customer support assistant.

Answer the customer's question based on the provided context.
Be friendly, clear and concise.

If the answer is not clearly in the context, try to give the best answer you can based on available information.
Only if the topic is completely unrelated, say: "I'm sorry, I don't have information about that. Please contact our support team."

Chat History:
{history_text}

Context:
{context}

Customer Question:
{question}
"""
    return prompt


def extract_sources(retrieve_docs):
    seen = set()
    sources = []

    for doc in retrieve_docs:
        page = doc.metadata.get("page")
        source = doc.metadata.get("source")
        key = (source , page)

        if key not in seen:
            seen.add(key)
            sources.append({
                "page": page,
                "source": source
            })

    return sources


def ask_question(question: str, company_id: str, session_id: str):
    logger.info(f"Question received for company: {company_id}")
    
    history = get_history(session_id)
    docs = retrieve_document(question , company_id)
    logger.debug(f"Retreived {len(docs)} documents")

    if not docs:
        logger.warning(f"No document found for company: {company_id}")
        raise CompanyNotFoundError(company_id)
    
    context = build_content(docs)
    prompt = creat_prompt(question , context , history)

    try:
        answer = generate_answer(prompt)
    
    except Exception as e:
        logger.error(f"LLM failed: {str(e)}")
        raise LLMError(str(e))
    
    add_message(session_id , "user", question)
    add_message(session_id, "assistant", answer)

    save_question(company_id , question , answer)

    logger.info(f"Answer generated seccussfully")
    sources = extract_sources(docs)

    context = build_content(docs)
    print("=== CONTEXT ===")
    print(context[:1000])  # اول 1000 کاراکتر
    print("=== END CONTEXT ===")
    prompt = creat_prompt(question, context, history)

    return {
        "answer":answer,
        "sources":sources
    }


def ask_question_stream(question: str, company_id: str, session_id: str) -> Generator[str , None , None]:
    logger.info(f"Stream question received for company: {company_id}")

    history = get_history(session_id)
    docs = retrieve_document(question , company_id)

    if not docs:
        logger.warning(f"No document found for company: {company_id}")
        raise CompanyNotFoundError(company_id)

    context = build_content(docs)
    prompt = creat_prompt(question , context , history)

    full_answer = ""

    for token in generate_answer_stream(prompt):
        full_answer += token
        yield token

    add_message(session_id , "user" , question)
    add_message(session_id, "assistant" , full_answer)

    save_question(company_id , question , full_answer)

    logger.info("Stream answer completed")
