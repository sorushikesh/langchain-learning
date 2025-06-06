import logging

from fastapi import APIRouter, HTTPException, Query, Depends

from app_wikipedia_scraping.dependencies.dependencies import get_wikipedia_service
from app_wikipedia_scraping.schemas.response import WikipediaSummaryResponse
from app_wikipedia_scraping.service.wikipedia_service import WikipediaService

router = APIRouter(prefix="/wikipedia", tags=["wikipedia"])

logger = logging.getLogger()


@router.get("/summary", response_model=WikipediaSummaryResponse)
def fetch_wikipedia_summary(
        query: str = Query(...),
        service: WikipediaService = Depends(get_wikipedia_service)
):
    try:
        service.__init__()
        summary_text = service.get_summarise_content(query)
        logger.info("Text summaries successfully")
        return WikipediaSummaryResponse(query=query, summary=summary_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
