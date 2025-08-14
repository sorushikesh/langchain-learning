from app.util.config import ModelDetails
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=ModelDetails.AZURE_ENDPOINT,
    azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
    api_key=ModelDetails.AZURE_API_KEY,
    api_version=ModelDetails.AZURE_API_VERSION,
    temperature=1
)

question = "Which is most latest capital city ?"
output = llm.invoke(question)

print(f"Question : {question}")
print(f"LLM output :  {output}")

print(f"Content : {output.content}")
