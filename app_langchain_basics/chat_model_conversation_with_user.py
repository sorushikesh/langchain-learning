from app.util.config import ModelDetails
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=ModelDetails.AZURE_ENDPOINT,
    azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
    api_key=ModelDetails.AZURE_API_KEY,
    api_version=ModelDetails.AZURE_API_VERSION,
    temperature=1
)

chat_history = []
system_message = SystemMessage(content="You are an expert in geo-politics")
chat_history.append(system_message)

while True:
    query = input("User input : ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    result = llm.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))
    print(f"AI response {response}")

print(f"Chat history : {chat_history}")
