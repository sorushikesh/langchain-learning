from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from app.constants.config import ModelDetails

llm = AzureChatOpenAI(
    azure_endpoint=ModelDetails.AZURE_ENDPOINT,
    azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
    api_key=ModelDetails.AZURE_API_KEY,
    api_version=ModelDetails.AZURE_API_VERSION,
    temperature=1
)

title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Generate 3 creative blog post titles about {topic}"
)
title_chain = LLMChain(
    llm=llm,
    prompt=title_prompt
)

content_prompt = PromptTemplate(
    input_variables=["title"],
    template="Write a short and engaging blog post for title: {title}"
)
content_chain = LLMChain(
    llm=llm,
    prompt=content_prompt
)

multi_chain = SimpleSequentialChain(
    chains=[title_chain, content_chain],
    verbose=True
)

if __name__ == "__main__":
    topic = "artificial intelligence in healthcare"
    result = multi_chain.run(topic)
    print(result)
