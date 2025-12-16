# import langchain
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from app.agents.agent import run_agent

load_dotenv()
# langchain.verbose = False
# langchain.debug = False
# langchain.llm_cache = False

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/agent")
async def run_ai_agent(query: str):
    run_agent(query=query)
    return {"status": "Agent run successfully"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )