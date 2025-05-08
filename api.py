# python -m uvicorn api:app --reload
# $env:GOOGLE_APPLICATION_CREDENTIALS=C:\Users\parth\Desktop\Cerebry\video-ai-tutor\backend\cerebryai-1cf9ad8980f2.json
# C:\Users\parth\Desktop\Cerebry\video-ai-tutor\backend\venv\Scripts\python.exe -m pip freeze > requirements.txt
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retrieve_db import get_session, store_conversation
from main import llm_response
from typing import Optional
import logging
import store_db
# Set up basic configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\parth\Desktop\Cerebry\video-ai-tutor\backend\cerebryai-1cf9ad8980f2.json"
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SessionData(BaseModel):
    session_id: int
    conversation_history: str


@app.get("/")
async def root():
    return {"message": "Backend started to run"}

@app.post("/session")
async def fetch_session(session_id: str = Form(...)):
    """
    Called first to load full conversation history.
    """
    logging.info(f"Received session ID: {session_id}")
    history = get_session(session_id)
    
    return {"session_id": session_id, "conversation_history": history}


@app.post("/model_response")
async def model_response(
    video_id: str = Form(...),
    session_id: str = Form(...),
    text_query: str = Form(...),
    image_query: Optional[UploadFile] = File(None)
):
    logging.info(f"Received Query from Frontend")

    image_query = await image_query.read() if image_query else None

    if image_query is None: 
        logging.info(f"Image query is None")
    else:
        logging.info(f"Type of image query: {type(image_query)}")
        logging.info(f"Image Exists")

    response = llm_response(video_id, text_query, image_query)
    logging.info(f"Response from LLM: {response}")
    logging.info("Finished calling the llm_response function")

    logging.info("Lets begin with storing the one by one conversation")
    store_conversation(session_id, response, text_query, image_query)

    return {"message": response}

@app.post("/validate_user")
async def validate_user(
    email: str = Form(...),
    password: str = Form(...)
):
    logging.info(f"Received user validation request")
    response = store_db.validate_user(email, password)
    logging.info(f"Response from user validation: {response}")
    return {"message": response}
