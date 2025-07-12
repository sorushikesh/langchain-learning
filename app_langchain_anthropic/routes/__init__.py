from fastapi import APIRouter

from app_langchain_anthropic.routes.ask import router as ask_router


router = APIRouter()
router.include_router(ask_router, prefix="/chat", tags=["Chat"])
