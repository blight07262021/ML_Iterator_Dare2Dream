# 🤖 Insight AI: Generative AI Market Research Platform

**Insight AI** is a full-stack platform that uses **Generative AI** to automate **qualitative market research**.  
It dramatically reduces the time and cost of traditional methods by conducting **AI-driven interviews**, generating **real-time summaries**, and enabling **deep insight discovery** through an interactive **Q&A bot**.

---
🎥 [Watch Project Demo](https://drive.google.com/file/d/1tQxIC6TF5igCLpBx5gw4qaZEmbKl9H4n/view?usp=drivesdk )


## 🚀 Key Features

- **Dynamic AI Interviews** — Conducts automated, adaptive conversational interviews 24/7.  
- **Real-Time Summarization** — Instantly generates AI-powered summaries for interviews and projects.  
- **RAG-Powered Q&A Bot** — Ask complex questions in plain language and get context-aware answers from your research data.  
- **Vector Database Integration** — Uses **ChromaDB** for efficient Retrieval-Augmented Generation (RAG).  
- **Accessibility Focused** — Integrated **Text-to-Speech (TTS)** for all AI responses.  
- **Project Dashboard** — A central hub to create, manage, and share research projects.

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Tailwind CSS, Chart.js |
| **Backend** | FastAPI, LangChain, Groq (Llama 3.1), SQLAlchemy |
| **Databases** | MySQL, ChromaDB |

---

## 🏗️ System Architecture

- **Frontend (SPA)** → The user-facing application for project management and AI interaction.  
- **Backend (FastAPI)** → The core API for business logic, LLM orchestration, and database management.  
- **LLM Service (LangChain & Groq)** → Powers all generative AI tasks, from interviews to Q&A.  
- **Databases (MySQL & ChromaDB)** →  
  - MySQL stores project and user data.  
  - ChromaDB manages vector embeddings for RAG-based insights.

---

## ⚙️ Setup Instructions

### File structure

insight-ai/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py         # Makes the 'app' directory a Python package
│   │   ├── crud.py             # Handles database create, read, update, delete operations
│   │   ├── database.py         # Configures the connection to the MySQL database
│   │   ├── llm_service.py      # Contains all logic for interacting with the LLM (LangChain, Groq)
│   │   ├── main.py             # The main FastAPI application file, defines API endpoints
│   │   ├── models.py           # Defines SQLAlchemy ORM models and Pydantic schemas
│   │   └── vector_db_service.py# Manages interactions with the ChromaDB vector database
│   │
│   ├── .env                    # Stores environment variables like API keys (not in version control)
│   └── requirements.txt        # Lists all Python dependencies for the backend
│
├── frontend/
│   ├── index.html              # The main project dashboard page
│   ├── app.js                  # JavaScript for the main dashboard
│   ├── interview.html          # The page for conducting an AI interview
│   ├── chat.js                 # JavaScript for the interview chat interface
│   ├── qa_bot.html             # The page for the question-answering bot
│   ├── qa_bot.js               # JavaScript for the Q&A bot interface
│   └── style.css               # Shared CSS for all frontend pages
│
└── README.md                   # The main project documentation file for your repository

### 1️⃣ Backend Setup

'''bash
# Clone the repository and navigate to the backend
git clone https://github.com/your-username/insight-ai.git
cd insight-ai/backend

# Create and activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt




##  Create a .env file in backend/app with your Groq API key:
GROQ_API_KEY="your_api_key_here"

## Run the FastAPI server:
uvicorn app.main:app --reload

## 📖 Usage Guide

1. **Create Project** — Define your research goals on the dashboard.  
2. **Share Link** — Distribute the generated interview link to participants.  
3. **Monitor Progress** — Track completed interviews and AI summaries in real-time.  
4. **Analyze Insights** — Use the Q&A bot to explore your qualitative data.  
5. **Sync Summaries** — Push processed summaries to the vector DB for RAG queries.  
6. **Ask Questions** — Query your research data conversationally and get instant, insightful answers.
