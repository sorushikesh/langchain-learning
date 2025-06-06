from fastapi import FastAPI

from app_langchain_chat_model.model.models import ChatResponse, ChatRequest
from app_langchain_chat_model.service.chat_service import chat_with_model

app = FastAPI(title="LangChain ChatModel API")


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    response_text = chat_with_model(request.message)
    return ChatResponse(response=response_text)
