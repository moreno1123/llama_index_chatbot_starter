from dotenv import load_dotenv

load_dotenv()

import logging
import os
import uvicorn
from app.api.routes import chat, chat_no_stream
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set

if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust as needed for security in a production environment
        allow_methods=["*"],
    )

app.include_router(chat.chat_router, prefix="/api/chat")
app.include_router(chat_no_stream.chat_no_stream_router, prefix="/api/chat_no_stream")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
