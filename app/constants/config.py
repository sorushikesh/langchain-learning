import os
from dotenv import load_dotenv

load_dotenv()

class ModelDetails:
    """
    Configuration for Azure OpenAI
    """
    AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
