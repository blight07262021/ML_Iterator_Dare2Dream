# import os
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import JSONResponse, StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from typing import List
# import io # Import io
# from gtts import gTTS # Import gTTS

# from . import crud, models, llm_service
# from .database import SessionLocal, engine, Base

# # === Create database tables ===
# Base.metadata.create_all(bind=engine)

# # === Initialize FastAPI app ===
# app = FastAPI(title="AI Market Research PoC")


# # === Enable CORS (for frontend-backend communication) ===
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # WARNING: For development only. Restrict in production.
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # === Database Dependency ===
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # =======================
# #       API ROUTES
# # =======================
# # New TTS Endpoint
# @app.post("/api/tts")
# async def text_to_speech(request: models.TTSRequest):
#     """
#     Converts provided text to speech using gTTS and returns an MP3 audio file.
#     """
#     if not request.text:
#         raise HTTPException(status_code=400, detail="Text cannot be empty for TTS.")

#     try:
#         tts = gTTS(text=request.text, lang='en', slow=False)
#         # Use BytesIO to store the audio in memory
#         audio_stream = io.BytesIO()
#         tts.write_to_fp(audio_stream)
#         audio_stream.seek(0) # Rewind the stream to the beginning

#         return StreamingResponse(audio_stream, media_type="audio/mpeg", 
#                                  headers={"Content-Disposition": "attachment; filename=\"summary.mp3\""})
#     except Exception as e:
#         print(f"Error generating TTS: {e}")
#         raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")

# @app.post("/api/projects", response_model=models.ProjectModel)
# def create_project(project: models.ProjectCreate, db: Session = Depends(get_db)):
#     """Create a new market research project."""
#     return crud.create_project(db=db, project=project)


# @app.get("/api/projects", response_model=List[models.ProjectModel])
# def read_projects(db: Session = Depends(get_db)):
#     """Retrieve all projects."""
#     return crud.get_projects(db)


# @app.post("/api/interviews")
# def start_interview(interview_data: models.InterviewCreate, db: Session = Depends(get_db)):
#     """Start a new interview session for a project."""
#     project = crud.get_project(db, project_id=interview_data.project_id)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")

#     interview = crud.create_interview(db, project_id=interview_data.project_id)

#     project_context = {
#         "company_description": project.company_description,
#         "product_idea": project.product_idea,
#         "target_audience": project.target_audience,
#         "core_problem": project.core_problem,
#     }
#     first_question = llm_service.get_initial_question(project_context)
#     crud.save_message(db, interview.id, 'ai', first_question)

#     return {"interview_id": interview.id, "first_question": first_question}


# @app.post("/api/interviews/{interview_id}/message")
# def handle_user_message(interview_id: int, message: models.MessagePayload, db: Session = Depends(get_db)):
#     """Handle user replies and generate AI responses."""
#     crud.save_message(db, interview_id, 'user', message.content)

#     messages_orm = crud.get_interview_messages(db, interview_id)
#     conversation_history = [{"sender": msg.sender, "content": msg.content} for msg in messages_orm]

#     user_message_count = len([msg for msg in conversation_history if msg['sender'] == 'user'])
#     if user_message_count >= 5: # Summarize after 5 user responses
#         summary_text = llm_service.get_summary(conversation_history)

#         # --- MODIFIED ---
#         # Call the new function to save the summary in the new table
#         crud.create_session_summary(db, interview_id, summary_text)

        

#         final_message = "Thank you so much for your time and valuable insights! This concludes our interview."
#         return {"response": final_message, "status": "completed"}
#     else:
#         ai_response = llm_service.get_probing_question(conversation_history)
#         crud.save_message(db, interview_id, 'ai', ai_response)
#         return {"response": ai_response, "status": "in_progress"}


# # ===============================
# #   PROJECT SUMMARY ROUTE
# # ===============================

# @app.post("/api/projects/{project_id}/generate_summary")
# def generate_project_summary_endpoint(project_id: int, db: Session = Depends(get_db)):
#     """
#     Generates a hierarchical summary for a specific project.
#     """
#     try:
#         # Call the updated function from the llm_service
#         summary = llm_service.generate_project_summary(project_id=project_id)
#         return {"status": "success", "final_summary": summary}
#     except Exception as e:
#         print(f"Error generating summary for project {project_id}: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# # =======================
# #     FRONTEND MOUNT
# # =======================
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# frontend_dir = os.path.join(PROJECT_ROOT, "frontend")

# if os.path.exists(frontend_dir):
#     print(f"✅ Found frontend directory at: {frontend_dir}")
#     app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
# else:
#     print(f"⚠️  Frontend directory not found at {frontend_dir} — skipping static mount.")


import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import io 
from gtts import gTTS

from . import crud, models, llm_service, vector_db_service
from .database import SessionLocal, engine, Base

# === Create database tables ===
Base.metadata.create_all(bind=engine)

# === Initialize FastAPI app ===
app = FastAPI(title="AI Market Research PoC")


# === Enable CORS (for frontend-backend communication) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Database Dependency ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =======================
#       API ROUTES
# =======================
@app.post("/api/tts")
async def text_to_speech(request: models.TTSRequest):
    """
    Converts provided text to speech using gTTS and returns an MP3 audio file.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty for TTS.")

    try:
        tts = gTTS(text=request.text, lang='en', slow=False)
        audio_stream = io.BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)

        return StreamingResponse(audio_stream, media_type="audio/mpeg", 
                                 headers={"Content-Disposition": "attachment; filename=\"summary.mp3\""})
    except Exception as e:
        print(f"Error generating TTS: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")

@app.post("/api/projects", response_model=models.ProjectModel)
def create_project(project: models.ProjectCreate, db: Session = Depends(get_db)):
    """Create a new market research project."""
    return crud.create_project(db=db, project=project)


@app.get("/api/projects", response_model=List[models.ProjectModel])
def read_projects(db: Session = Depends(get_db)):
    """Retrieve all projects."""
    return crud.get_projects(db)


@app.post("/api/interviews")
def start_interview(interview_data: models.InterviewCreate, db: Session = Depends(get_db)):
    """Start a new interview session for a project."""
    project = crud.get_project(db, project_id=interview_data.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    interview = crud.create_interview(db, project_id=interview_data.project_id)

    project_context = {
        "company_description": project.company_description,
        "product_idea": project.product_idea,
        "target_audience": project.target_audience,
        "core_problem": project.core_problem,
    }
    first_question = llm_service.get_initial_question(project_context)
    crud.save_message(db, interview.id, 'ai', first_question)

    return {"interview_id": interview.id, "first_question": first_question}


@app.post("/api/interviews/{interview_id}/message")
def handle_user_message(interview_id: int, message: models.MessagePayload, db: Session = Depends(get_db)):
    """Handle user replies and generate AI responses."""
    crud.save_message(db, interview_id, 'user', message.content)

    messages_orm = crud.get_interview_messages(db, interview_id)
    conversation_history = [{"sender": msg.sender, "content": msg.content} for msg in messages_orm]

    user_message_count = len([msg for msg in conversation_history if msg['sender'] == 'user'])
    if user_message_count >= 7: 
        summary_text = llm_service.get_summary(conversation_history)
        crud.create_session_summary(db, interview_id, summary_text)
        final_message = "Thank you so much for your time and valuable insights! This concludes our interview."
        return {"response": final_message, "status": "completed"}
    else:
        ai_response = llm_service.get_probing_question(conversation_history)
        crud.save_message(db, interview_id, 'ai', ai_response)
        return {"response": ai_response, "status": "in_progress"}

@app.post("/api/projects/{project_id}/generate_summary")
def generate_project_summary_endpoint(project_id: int, db: Session = Depends(get_db)):
    """
    Generates a hierarchical summary for a specific project.
    """
    try:
        summary = llm_service.generate_project_summary(project_id=project_id)
        return {"status": "success", "final_summary": summary}
    except Exception as e:
        print(f"Error generating summary for project {project_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===========================
#   NEW INSIGHTS Q&A ROUTES
# ===========================

@app.post("/api/projects/{project_id}/sync_summaries")
def sync_project_summaries_endpoint(project_id: int):
    """
    Triggers the process of fetching summaries, creating embeddings,
    and storing them in the ChromaDB vector database.
    """
    try:
        result = vector_db_service.sync_project_summaries(project_id)
        return JSONResponse(content=result)
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Error syncing summaries for project {project_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during sync: {e}")


# Pydantic model for the question payload
class QuestionPayload(models.BaseModel):
    question: str

@app.post("/api/projects/{project_id}/ask")
def ask_question_endpoint(project_id: int, payload: QuestionPayload, db: Session = Depends(get_db)):
    """
    Handles a user's question by querying the vector database for context
    and generating a final answer with the LLM.
    """
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not payload.question or not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        answer = llm_service.get_answer_from_insights(project_id, payload.question)
        return {"answer": answer}
    except Exception as e:
        print(f"Error answering question for project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate an answer from insights.")

# =======================
#     FRONTEND MOUNT
# =======================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_dir = os.path.join(PROJECT_ROOT, "frontend")

if os.path.exists(frontend_dir):
    print(f"✅ Found frontend directory at: {frontend_dir}")
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
else:
    print(f"⚠️  Frontend directory not found at {frontend_dir} — skipping static mount.")


# import os
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import JSONResponse, StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from typing import List
# import io 
# from gtts import gTTS

# from . import crud, models, llm_service, vector_db_service
# from .database import SessionLocal, engine, Base

# # === Create database tables ===
# Base.metadata.create_all(bind=engine)

# # === Initialize FastAPI app ===
# app = FastAPI(title="AI Market Research PoC")

# # === CORS Middleware ===
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # === Database Dependency ===
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # =======================
# #       API ROUTES
# # =======================
# @app.post("/api/tts")
# async def text_to_speech(request: models.TTSRequest):
#     if not request.text:
#         raise HTTPException(status_code=400, detail="Text cannot be empty for TTS.")
#     try:
#         tts = gTTS(text=request.text, lang='en', slow=False)
#         audio_stream = io.BytesIO()
#         tts.write_to_fp(audio_stream)
#         audio_stream.seek(0)
#         return StreamingResponse(audio_stream, media_type="audio/mpeg")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")

# @app.post("/api/projects", response_model=models.ProjectModel)
# def create_project(project: models.ProjectCreate, db: Session = Depends(get_db)):
#     return crud.create_project(db=db, project=project)

# @app.get("/api/projects", response_model=List[models.ProjectModel])
# def read_projects(db: Session = Depends(get_db)):
#     return crud.get_projects(db)

# @app.post("/api/interviews")
# def start_interview(interview_data: models.InterviewCreate, db: Session = Depends(get_db)):
#     project = crud.get_project(db, project_id=interview_data.project_id)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")
#     interview = crud.create_interview(db, project_id=interview_data.project_id)
#     project_context = {
#         "company_description": project.company_description,
#         "product_idea": project.product_idea,
#         "target_audience": project.target_audience,
#         "core_problem": project.core_problem,
#     }
#     first_question = llm_service.get_initial_question(project_context)
#     crud.save_message(db, interview.id, 'ai', first_question)
#     return {"interview_id": interview.id, "first_question": first_question}

# @app.post("/api/interviews/{interview_id}/message")
# def handle_user_message(interview_id: int, message: models.MessagePayload, db: Session = Depends(get_db)):
#     """
#     Handle user replies and generate AI responses using the new intelligent ending logic.
#     """
#     crud.save_message(db, interview_id, 'user', message.content)
    
#     # --- 1. Get conversation history and project context ---
#     messages_orm = crud.get_interview_messages(db, interview_id)
#     conversation_history = [{"sender": msg.sender, "content": msg.content} for msg in messages_orm]
    
#     interview = crud.get_interview(db, interview_id)
#     if not interview:
#         raise HTTPException(status_code=404, detail="Interview not found")
#     project = crud.get_project(db, interview.project_id)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project associated with interview not found")

#     project_context = {
#         "company_description": project.company_description,
#         "product_idea": project.product_idea,
#         "target_audience": project.target_audience,
#         "core_problem": project.core_problem,
#     }

#     # --- 2. Check hard limit condition ---
#     ai_question_count = len([msg for msg in conversation_history if msg['sender'] == 'ai'])
#     force_end = ai_question_count >= 15

#     # --- 3. Get next step from LLM (unless forcing end) ---
#     if not force_end:
#         next_step = llm_service.get_next_step(project_context, conversation_history)
#     else:
#         next_step = {"is_complete": True, "next_question": ""} # Prepare for forced ending

#     # --- 4. Process the decision ---
#     if next_step.get("is_complete"):
#         summary_text = llm_service.get_summary(conversation_history)
#         crud.create_session_summary(db, interview_id, summary_text)
        
#         final_message = next_step.get("next_question") or "Thank you for your time. This concludes our interview."
#         if force_end and not next_step.get("next_question"):
#              final_message = "We've reached the end of our session. Thank you so much for your detailed feedback!"

#         crud.save_message(db, interview_id, 'ai', final_message) # Save the final message
#         return {"response": final_message, "status": "completed"}
#     else:
#         ai_response = next_step.get("next_question", "Could you please elaborate on that?")
#         crud.save_message(db, interview_id, 'ai', ai_response)
#         return {"response": ai_response, "status": "in_progress"}

# @app.post("/api/projects/{project_id}/generate_summary")
# def generate_project_summary_endpoint(project_id: int, db: Session = Depends(get_db)):
#     try:
#         summary = llm_service.generate_project_summary(project_id=project_id)
#         return {"status": "success", "final_summary": summary}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ===========================
# #   INSIGHTS Q&A ROUTES
# # ===========================
# @app.post("/api/projects/{project_id}/sync_summaries")
# def sync_project_summaries_endpoint(project_id: int):
#     try:
#         result = vector_db_service.sync_project_summaries(project_id)
#         return JSONResponse(content=result)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred during sync: {e}")

# class QuestionPayload(models.BaseModel):
#     question: str

# @app.post("/api/projects/{project_id}/ask")
# def ask_question_endpoint(project_id: int, payload: QuestionPayload, db: Session = Depends(get_db)):
#     project = crud.get_project(db, project_id)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")
#     try:
#         answer = llm_service.get_answer_from_insights(project_id, payload.question)
#         return {"answer": answer}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Failed to generate an answer from insights.")

# # =======================
# #     FRONTEND MOUNT
# # =======================
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# frontend_dir = os.path.join(PROJECT_ROOT, "frontend")
# if os.path.exists(frontend_dir):
#     app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")



