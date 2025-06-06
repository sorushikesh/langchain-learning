"""
Main class for playground
"""
from app_wikipedia_scraping.wikipedia.fetch_details import fetch_details

if __name__ == "__main__":
    content = fetch_details("Cristiano Ronaldo")
    print(content)