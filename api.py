import json
from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from retrieve_db import get_session, store_conversation
from main import llm_response
from typing import Optional

app = FastAPI()

class SessionData(BaseModel):
    session_id: int
    conversation_history: str


@app.get("/")
async def root():
    return {"message": "Backend started to run"}

@app.get("/session/{session_id}")
async def fetch_session(session_id: int):
    """
    Called first to load full conversation history.
    """
    history = get_session(session_id)
    
    return {"session_id": session_id, "conversation_history": history}

@app.post("/store_session")
async def store_session(data: SessionData):
    """
    Called to store the session history.
    """
    # conversation_json = json.dumps([msg.dict() for msg in data.conversation_history])
    store_conversation(data.session_id, data.conversation_history)
    
    return "Conversation history stored successfully"

@app.post("/model_response")
async def model_response(
    video_id: str = Form(...),
    text_query: str = Form(...),
    image_query: Optional[UploadFile] = File(None)
):
    """
    Called after chat query. Will check cache and proceed.
    """
    image_query = await image_query.read() if image_query else None
    response = llm_response(video_id, text_query, image_query)
    return response