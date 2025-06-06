import logging

import wikipedia

logger = logging.getLogger()

def fetch_details(name):
    """
    Fetches the wikipedia page content for the given name.
    :param name: str - The title or name to search on Wikipedia
    :return: str - Page content or error message
    """
    try:
        wikipedia.set_lang("en")

        logger.info(f"Fetching information for {name}")
        page = wikipedia.page(name)
        return page.content

    except Exception as err:
        return f"An unexpected error occurred while fetching information for {name}: {str(err)}"