import sqlite3
from datetime import datetime
from app.core.config import settings
from app.core.logger import get_logger
import os

logger = get_logger("analytics")

def init_db():
    os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok = True)

    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp TEXT NOT NULL
                      )
                """)
    
    conn.commit()
    conn.close()
    logger.info("Database initialized seccussfully")

def save_question(company_id: str, question: str, answer: str):

    try:
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
                INSERT INTO questions (company_id, question, answer, timestamp)
                VALUES (?, ?, ?, ?)    
                    """,(
                company_id,
                question,
                answer,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")                 
        ))

        conn.commit()
        conn.close()
        logger.debug(f"Question saved for company: {company_id}")

    except Exception as e:
        logger.error(f"Failed to save question: {str(e)}")

def get_analytics(company_id: str):
    try:
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT COUNT(*) FROM questions WHERE company_id = ?
                       """, (company_id,))
        
        total_question = cursor.fetchone()[0]


        cursor.execute("""
                       SELECT question, answer, timestamp
                       FROM questions
                       WHERE company_id = ?
                       ORDER BY timestamp DESC
                       LIMIT 10
                    """, (company_id,))
        
        recent_questions = cursor.fetchall()
        conn.close()

        return {
            "total_question": total_question,
            "recent_question": [
                {
                    "question" : row[0],
                    "answer" : row[1],
                    "timestamp" : row[2]
                }
                for row in recent_questions
            ]
        }
    
    except Exception as e:
        logger.error(f"Failed to get analytics: {str(e)}")
        return {
            "total_question":0,
            "recent_question": []
        }