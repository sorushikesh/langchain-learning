import logging

from fastapi import APIRouter, HTTPException

from app.model.ChatRequest import ChatRequest
from app.model.ChatResponse import ChatResponse
from app_langchain_anthropic.langchain_pipeline import generate_response

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ask", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = generate_response(request.message)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
