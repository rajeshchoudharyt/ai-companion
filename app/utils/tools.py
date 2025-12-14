import os
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="llama-3.3-70b",
    model_provider="openai",
    base_url="https://api.cerebras.ai/v1",
    api_key=os.getenv("CEREBRAS_API_KEY")
)
