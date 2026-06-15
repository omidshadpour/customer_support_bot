# 🤖 Customer Support Bot

An AI-powered customer support chatbot that businesses can embed on their website. Upload your FAQ and policy documents, and let AI handle customer questions 24/7.

## 🚀 Live Demo
[Admin Panel](https://your-streamlit-url.streamlit.app)

## 🏗️ Architecture

```
Customer Question → Chat Widget → FastAPI → LangChain → ChromaDB → Groq LLM → Streaming Response
                                     ↓
                                  SQLite (Analytics)
```

## ✨ Features

- 🤖 **AI Chatbot** — Answers customer questions based on your documents
- 📄 **Document Upload** — Upload FAQ, policies, or any PDF document
- ⚡ **Streaming Response** — Real-time token-by-token answers like ChatGPT
- 🧠 **Chat Memory** — Remembers conversation history per session
- 📊 **Analytics Dashboard** — See what customers are asking about
- 🌐 **Embeddable Widget** — One line of code to add to any website
- 🏢 **Multi-Company Support** — Each company has isolated data
- 🛡️ **Error Handling** — Graceful error messages for all failure cases
- 📝 **Logging** — Full request/response logging

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| LLM | Groq (llama-3.3-70b) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB |
| Document Processing | LangChain |
| Analytics | SQLite |
| Admin Panel | Streamlit |
| Widget | HTML + JavaScript |

## 📁 Project Structure

```
customer_support_bot/
├── main.py                   # FastAPI entry point
├── app/
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── core/
│   │   ├── config.py         # Environment configuration
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── logger.py         # Logging setup
│   ├── services/
│   │   ├── ingestion.py      # PDF loading & chunking
│   │   ├── rag.py            # RAG pipeline
│   │   ├── retrieval.py      # Vector search
│   │   ├── memory.py         # Chat history
│   │   └── analytics.py      # Analytics & SQLite
│   ├── llm/
│   │   └── groq_service.py   # Groq LLM integration
│   ├── vector_store/
│   │   └── chroma_db.py      # ChromaDB setup
│   └── ui/
│       ├── admin.py          # Streamlit admin panel
│       └── widget.html       # Embeddable chat widget
├── requirements.txt
└── .env.example
```

## 🔧 Installation

**1. Clone the repository:**
```bash
git clone https://github.com/omidshadpour/customer-support-bot.git
cd customer-support-bot
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

**4. Run FastAPI:**
```bash
uvicorn main:app --reload
```

**5. Run Admin Panel:**
```bash
streamlit run app/ui/admin.py
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admin/upload` | Upload a PDF document |
| GET | `/admin/analytics/{company_id}` | Get company analytics |
| POST | `/chat/ask` | Ask a question (single response) |
| POST | `/chat/ask-stream` | Ask a question (streaming) |
| POST | `/chat/sources` | Get source pages |
| GET | `/widget/{company_id}` | Get embeddable chat widget |
| GET | `/docs` | Swagger UI |

## 🌐 Embedding the Widget

Add this one line to any website:

```html
<iframe src="http://your-api-url/widget/your_company_id" width="400" height="600" frameborder="0"></iframe>
```

## ⚙️ Environment Variables

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
CHROMA_PATH=chroma_db
COLLECTION_NAME=support_docs
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=100
RETRIEVAL_K=3
UPLOAD_DIR=uploads
LOGS_DIR=logs
DB_PATH=database/analytics.db
```

## 📊 How It Works

1. **Admin uploads** — PDF documents are loaded, split into 500-token chunks, and embedded
2. **Store** — Chunks stored in ChromaDB under company-specific collection
3. **Customer asks** — Question is embedded and matched against stored chunks
4. **Generate** — Top 3 chunks passed to Groq LLM as context
5. **Stream** — Answer streamed token by token to the chat widget
6. **Analytics** — Every question and answer saved to SQLite

## 🙋 Author

**Omid Shadpour**
- GitHub: [@omidshadpour](https://github.com/omidshadpour)

