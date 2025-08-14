import logging

import wikipedia
from app.util.config import Settings, ModelDetails
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from app.constants.templates import Templates

logger = logging.getLogger(__name__)


class WikipediaService:

    def __init__(self):
        self.language = Settings.WIKI_LANG
        wikipedia.set_lang(self.language)
        logger.info(f"Wikipedia language set to: {self.language}")

    def get_content(self, query: str) -> str:
        logger.info(f"Fetching full content for '{query}' from Wikipedia ({self.language})")
        return wikipedia.page(query).content

    def get_summarise_content(self, query: str):
        logger.info(f"Summarizing Wikipedia content for '{query}'")

        try:
            content = self.get_content(query)

            summary_prompt_template = PromptTemplate(
                input_variables=["content"],
                template=Templates.summarise_content
            )

            llm = AzureChatOpenAI(
                azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
                azure_endpoint=ModelDetails.AZURE_ENDPOINT,
                api_key=ModelDetails.AZURE_API_KEY,
                temperature=1,
                api_version=ModelDetails.AZURE_API_VERSION
            )

            chain = summary_prompt_template | llm
            response = chain.invoke({"content": content})

            return response.content

        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            return f"An error occurred: {str(e)}"
