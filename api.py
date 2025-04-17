from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from store_db import store_context_cache
from retrieve_db import get_session, get_cache_by_video
import uuid
import datetime

app = FastAPI()

# Request models
class Query(BaseModel):
    session_id: int
    query: str


@app.get("/session/{session_id}")
async def fetch_session(session_id: int):
    """
    Called first to load full conversation history.
    """
    history = get_session(session_id)
    if history is None:
        '''
            We can create a new session here if needed with empty conversation history
        '''
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"session_id": session_id, "conversation_history": history}


@app.post("/model_response")
async def model_response(query: Query):
    """
    Called after chat query. Will check cache and proceed.
    """
    cache = get_cache_by_video(query.session_id)

    if cache:
        return {
            "message": "Cache found",
            "cache": cache,
        }
    
    # Simulate generating a new cache
    new_cache_id = str(uuid.uuid4())
    ttl = "1h"

    # Store new cache entry
    store_context_cache(new_cache_id, query.session_id, ttl)

    return {
        "message": "New cache generated",
        "cache_id": new_cache_id,
        "session_id": query.session_id
    }
