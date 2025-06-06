import uvicorn
from fastapi import FastAPI

from app_wikipedia_scraping.routers.wikipedia_router import router as wikipedia_router

app = FastAPI(
    title="Wikipedia Info API with data summaries using LLM"
)

app.include_router(wikipedia_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
