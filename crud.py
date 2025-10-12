from sqlalchemy.orm import Session, joinedload
from . import models

# Project functions
def create_project(db: Session, project: models.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session):
    # --- MODIFIED ---
    # Eagerly load interviews and their summaries to prevent extra database queries
    return db.query(models.Project).options(
        joinedload(models.Project.interviews).joinedload(models.Interview.summary)
    ).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

# Interview functions
def create_interview(db: Session, project_id: int):
    db_interview = models.Interview(project_id=project_id)
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

def get_interview(db: Session, interview_id: int):
    return db.query(models.Interview).filter(models.Interview.id == interview_id).first()

# --- REPLACED save_interview_summary with create_session_summary ---
def create_session_summary(db: Session, interview_id: int, summary_text: str):
    """Creates a new summary in the session_summary table."""
    db_summary = models.SessionSummary(interview_id=interview_id, summary=summary_text)
    db.add(db_summary)

    # Also update the interview status
    db_interview = get_interview(db, interview_id)
    if db_interview:
        db_interview.status = "completed"

    db.commit()
    db.refresh(db_summary)
    return db_summary

# Message functions
def save_message(db: Session, interview_id: int, sender: str, content: str):
    db_message = models.Message(interview_id=interview_id, sender=sender, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_interview_messages(db: Session, interview_id: int):
    return db.query(models.Message).filter(models.Message.interview_id == interview_id).order_by(models.Message.timestamp).all()

def delete_interview_messages(db: Session, interview_id: int):
    """Deletes all messages associated with a specific interview."""
    db.query(models.Message).filter(models.Message.interview_id == interview_id).delete()
    db.commit()