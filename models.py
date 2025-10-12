from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship, Mapped
from .database import Base
from pydantic import BaseModel, field_validator
from typing import List, Optional

# --- NEW SQLAlchemy ORM Model ---
# Create a new table specifically for summaries
class SessionSummary(Base):
    __tablename__ = "session_summary"
    id = Column(Integer, primary_key=True, index=True)
    summary = Column(Text, nullable=False)
    interview_id = Column(Integer, ForeignKey("interviews.id"), unique=True) # unique=True for one-to-one
    interview = relationship("Interview", back_populates="summary")

# SQLAlchemy ORM Models
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    company_description = Column(Text, nullable=False)
    product_idea = Column(Text, nullable=False)
    target_audience = Column(Text, nullable=False)
    core_problem = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    interviews = relationship("Interview", back_populates="project", cascade="all, delete-orphan")

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String(50), default="in_progress")
    # --- REMOVED summary column ---
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    project = relationship("Project", back_populates="interviews")
    messages = relationship("Message", back_populates="interview", cascade="all, delete-orphan")
    # --- ADDED relationship to the new SessionSummary table ---
    summary = relationship("SessionSummary", back_populates="interview", uselist=False, cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    sender = Column(String(50))
    content = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    interview = relationship("Interview", back_populates="messages")


# Pydantic Models (for API validation)
class InterviewModel(BaseModel):
    id: int
    status: str
    summary: Optional[str] = None # We keep this as a string for the frontend

    # This validator transforms the SessionSummary object into a simple string
    # for the API response, so the frontend doesn't need to change.
    @field_validator('summary', mode='before')
    @classmethod
    def summary_obj_to_str(cls, v):
        if isinstance(v, SessionSummary):
            return v.summary
        return v

    class Config:
        from_attributes = True

class ProjectModel(BaseModel):
    id: int
    company_description: str
    product_idea: str
    target_audience: str
    core_problem: str
    interviews: List[InterviewModel] = []

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    company_description: str
    product_idea: str
    target_audience: str
    core_problem: str

class MessagePayload(BaseModel):
    content: str

class InterviewCreate(BaseModel):
    project_id: int

# Pydantic model for the incoming summary text
class TTSRequest(BaseModel):
    text: str