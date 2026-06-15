from groq import Groq
from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import LLMError
from typing import Generator

logger = get_logger("groq")
client = Groq(api_key= settings.GROQ_API_KEY)

def generate_answer(prompt:str) -> str:
    logger.debug(f"Sending prompt to Groq, length: {len(prompt)}")

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{
                "role": "user",
                "content" : prompt
            }],
            stream=False,
            max_tokens=500
        )

        answer = response.choices[0].message.content
        logger.debug(f"Groq responded, answer length: {len(answer)}")
        
        return answer
    
    except Exception as e:
        logger.error(f"g=Groq error: {str(e)}")
        raise LLMError(str(e))
    

def generate_answer_stream(prompt: str) -> Generator[str, None, None]:
    logger.debug(f"Sending streaming prompt to Groq, length: {len(prompt)}")

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            stream=True,
            max_tokens=500
        )

        for chunk in response:
            token = chunk.choices[0].delta.content
            if token:
                yield token

        logger.debug("Groq stream completed")

    except Exception as e:
        logger.error(f"g=Groq stram error: {str(e)}")
        raise LLMError(str(e))
    