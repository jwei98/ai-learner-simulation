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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
from services.claude_service import get_claude_service
from services.persona_service import get_available_personas

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up AI Tutor Training Platform...")
    # Validate API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("WARNING: ANTHROPIC_API_KEY not set. AI features will not work.")
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
    problem: str
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

@app.get("/api/personas")
async def get_personas():
    """Get available AI personas"""
    try:
        persona_ids = get_available_personas()
        
        # Transform persona IDs into display-friendly format
        personas = []
        for persona_id in persona_ids:
            # Convert snake_case to Title Case for display name
            display_name = persona_id.replace("_", " ").title()
            personas.append({
                "id": persona_id,
                "name": display_name
            })
        
        return {"personas": personas}
    except Exception as e:
        print(f"Error fetching personas: {e}")
        # Return fallback personas if there's an error
        return {
            "personas": [
                {"id": "struggling_sam", "name": "Struggling Sam"},
                {"id": "overconfident_olivia", "name": "Overconfident Olivia"},
                {"id": "anxious_alex", "name": "Anxious Alex"},
                {"id": "methodical_maya", "name": "Methodical Maya"}
            ]
        }

@app.post("/api/sessions/start")
async def start_session(session_data: SessionStart):
    session_id = str(uuid.uuid4())
    
    # Initialize session
    active_sessions[session_id] = {
        "id": session_id,
        "tutor_name": session_data.tutor_name,
        "problem": session_data.problem,
        "persona_type": session_data.persona_type,
        "messages": [],
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }
    
    # Get initial response from AI persona
    initial_message = {
        "content": f"Hello! I need help with this problem: {session_data.problem}",
        "sender": "tutor",
        "timestamp": datetime.now().isoformat()
    }
    
    active_sessions[session_id]["messages"].append(initial_message)
    
    # Get AI response
    try:
        claude_service = get_claude_service()
        initial_response = await claude_service.get_persona_response(
            messages=[initial_message],
            persona_type=session_data.persona_type,
            problem=session_data.problem
        )
    except Exception as e:
        print(f"Error getting initial response: {e}")
        initial_response = "Hi! I'm ready to work on this problem. Where should we start?"
    
    # Add AI response to history
    active_sessions[session_id]["messages"].append({
        "content": initial_response,
        "sender": "learner",
        "timestamp": datetime.now().isoformat()
    })
    
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
    
    # Get Claude Haiku response based on persona
    try:
        claude_service = get_claude_service()
        ai_response = await claude_service.get_persona_response(
            messages=session["messages"],
            persona_type=session["persona_type"],
            problem=session["problem"]
        )
    except Exception as e:
        print(f"Error getting AI response: {e}")
        ai_response = "I'm having trouble understanding. Can you explain that differently?"
    
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
    
    # Get scoring from Claude Sonnet
    try:
        claude_service = get_claude_service()
        scores = await claude_service.get_session_scores(
            conversation_history=session["messages"],
            persona_type=session["persona_type"],
            problem=session["problem"]
        )
    except Exception as e:
        print(f"Error getting scores: {e}")
        scores = {
            "scores": {
                "explanation_clarity": 3,
                "patience_encouragement": 3,
                "active_questioning": 3,
                "adaptability": 3,
                "mathematical_accuracy": 3
            },
            "feedback": "Session completed. Unable to generate detailed feedback.",
            "session_summary": "The tutoring session has ended."
        }
    
    return scores

# Serve React app in production
if os.path.exists("../static"):
    app.mount("/", StaticFiles(directory="../static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)