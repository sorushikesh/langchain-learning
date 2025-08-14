from app.util.config import ModelDetails
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI

from app.constants.templates import Templates

llm = AzureChatOpenAI(
    azure_endpoint=ModelDetails.AZURE_ENDPOINT,
    azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
    api_key=ModelDetails.AZURE_API_KEY,
    api_version=ModelDetails.AZURE_API_VERSION,
    temperature=1
)


def chat_with_model(user_message: str) -> str:
    message = [
        SystemMessage(content=Templates.system_message_chat_model),
        HumanMessage(content=user_message)
    ]

    response = llm.invoke(message)
    return response.content
