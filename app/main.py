# import langchain
import uvicorn
import os
import json
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


class Agent(BaseModel):
    id: str
    query: str

@app.post("/agent/")
async def run_ai_agent(user: Agent):
    try:
        config: RunnableConfig = {"configurable": { "thread_id": user.id}} 

        agent = run_agent(query=user.query, config=config)
        agent_state = agent.get_state(config).values
        
        print("store", json.dumps(agent_state, indent=2))

    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return { "data": agent_state }


# Server config
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )