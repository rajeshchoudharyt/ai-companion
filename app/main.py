# import langchain
import uvicorn
import os
import json
import openai

from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

load_dotenv(os.path.join('..', '.env'))

from app.agents.agent import run_agent

# langchain.verbose = False
# langchain.debug = False
# langchain.llm_cache = False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


class User(BaseModel):
    id: str
    query: str


@app.post("/agent/")
async def run_ai_agent(user: User):
    memory = {}
    try:
        memory = run_agent(query=user.query, user_id=user.id)
    except openai.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit error")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return memory


# Server config
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )