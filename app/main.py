import langchain
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv()
langchain.verbose = False
langchain.debug = False
langchain.llm_cache = False

from app.utils.tools import llm

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )