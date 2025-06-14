from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
import uuid
from typing import Dict, List, Optional
from datetime import datetime
import json

# Import routers (to be created)
# from routers import sessions, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up AI Tutor Training Platform...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="AI Tutor Training Platform",
    description="Platform for training tutors with AI-simulated students",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (will migrate to PostgreSQL)
active_sessions: Dict[str, dict] = {}

# Pydantic models
class SessionStart(BaseModel):
    tutor_name: str
    math_problem: str
    persona_type: str

class Message(BaseModel):
    message: str
    sender: str

class SessionResponse(BaseModel):
    session_id: str
    initial_response: str
    persona_info: dict

# API endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/sessions/start")
async def start_session(session_data: SessionStart):
    session_id = str(uuid.uuid4())
    
    # Initialize session
    active_sessions[session_id] = {
        "id": session_id,
        "tutor_name": session_data.tutor_name,
        "math_problem": session_data.math_problem,
        "persona_type": session_data.persona_type,
        "messages": [],
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }
    
    # TODO: Initialize Claude conversation with persona
    initial_response = f"Hi! I'm ready to work on this problem: {session_data.math_problem}"
    
    return SessionResponse(
        session_id=session_id,
        initial_response=initial_response,
        persona_info={
            "name": session_data.persona_type.replace("_", " ").title(),
            "type": session_data.persona_type
        }
    )

@app.post("/api/sessions/{session_id}/message")
async def send_message(session_id: str, message: Message):
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    
    # Add message to history
    session["messages"].append({
        "content": message.message,
        "sender": message.sender,
        "timestamp": datetime.now().isoformat()
    })
    
    # TODO: Get Claude Haiku response based on persona
    ai_response = "I understand what you're saying. Let me think about that..."
    
    # Add AI response to history
    session["messages"].append({
        "content": ai_response,
        "sender": "learner",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "response": ai_response,
        "session_active": session["is_active"]
    }

@app.post("/api/sessions/{session_id}/end")
async def end_session(session_id: str):
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    session["is_active"] = False
    session["ended_at"] = datetime.now().isoformat()
    
    # TODO: Get scoring from Claude Sonnet
    scores = {
        "scores": {
            "explanation_clarity": 4,
            "patience_encouragement": 5,
            "active_questioning": 3,
            "adaptability": 4,
            "mathematical_accuracy": 5
        },
        "feedback": "Great job! You showed excellent patience with the student.",
        "session_summary": "The tutor successfully helped the student understand the concept."
    }
    
    return scores

# Serve React app in production
if os.path.exists("../static"):
    app.mount("/", StaticFiles(directory="../static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)