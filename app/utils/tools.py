import os
from langchain.chat_models import init_chat_model

models = {
    "default": "gpt-oss-120b",
    "response": "llama-3.3-70b"
}

llm = None

def get_llm(model = ["default", "response"]):
    llm = init_chat_model(
        model=models[model],
        model_provider="openai",
        base_url="https://api.cerebras.ai/v1",
        api_key=os.getenv("CEREBRAS_API_KEY"),
    )

    return llm
