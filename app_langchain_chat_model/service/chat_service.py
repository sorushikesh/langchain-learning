from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI

from app.constants.config import ModelDetails

llm = AzureChatOpenAI(
    azure_endpoint=ModelDetails.AZURE_ENDPOINT,
    azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
    api_key=ModelDetails.AZURE_API_KEY,
    api_version=ModelDetails.AZURE_API_VERSION,
    temperature=1
)

system_message_template = ("You are a knowledgeable and helpful assistant specializing in providing accurate, "
                           "up-to-date responses about sports events, teams, athletes, and historical sports facts. "
                           "Ensure your answers are clear, engaging, and relevant to the user's query.")


def chat_with_model(user_message: str) -> str:
    message = [
        SystemMessage(content=system_message_template),
        HumanMessage(content=user_message)
    ]

    response = llm.invoke(message)
    return response.content
