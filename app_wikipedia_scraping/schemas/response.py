from pydantic import BaseModel


class WikipediaSummaryResponse(BaseModel):
    query: str
    summary: str
