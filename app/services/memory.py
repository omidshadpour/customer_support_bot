from collections import defaultdict

chat_memory = defaultdict(list)

def add_message(session_id: str, role: str, content: str):
    chat_memory[session_id].append({
        "role": role,
        "content": content
    })

def get_history(session_id: str):
    return chat_memory[session_id]

def clear_history(session_id: str):
    chat_memory[session_id] = []

def get_all_sessions():
    return list(chat_memory.keys())