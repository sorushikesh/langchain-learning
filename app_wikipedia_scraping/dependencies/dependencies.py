from app_wikipedia_scraping.service.wikipedia_service import WikipediaService


def get_wikipedia_service() -> WikipediaService:
    return WikipediaService()
