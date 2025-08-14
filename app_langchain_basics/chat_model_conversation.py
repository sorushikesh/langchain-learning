from app.util.config import ModelDetails
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI

messages = [
    SystemMessage("You are an expert in geo-politics"),
    HumanMessage("Give short note about gulf of africa"),
]

llm = AzureChatOpenAI(
    azure_endpoint=ModelDetails.AZURE_ENDPOINT,
    azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
    api_key=ModelDetails.AZURE_API_KEY,
    api_version=ModelDetails.AZURE_API_VERSION,
    temperature=1
)

result = llm.invoke(messages)

print(f"Result content : {result.content}")
