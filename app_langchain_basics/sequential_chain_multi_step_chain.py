from app.util.config import ModelDetails
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

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
    prompt=title_prompt,
    output_key="title"
)

content_prompt = PromptTemplate(
    input_variables=["title"],
    template="Write a short and engaging blog post for title: {title}"
)
content_chain = LLMChain(
    llm=llm,
    prompt=content_prompt,
    output_key="content"
)

summary_prompt = PromptTemplate(
    input_variables=["title", "content"],
    template="Write short summary for title {title} and content {content}"
)
summary_chain = LLMChain(
    llm=llm,
    prompt=summary_prompt,
    output_key="summary"
)

multi_chain = SequentialChain(
    chains=[title_chain, content_chain, summary_chain],
    input_variables=["topic"],
    output_variables=["title", "content", "summary"],
    verbose=True
)

if __name__ == "__main__":
    topic = "artificial intelligence in healthcare"
    result = multi_chain.invoke({"topic": topic})
    print(f"Title : {result["title"]}")
    print(f"Content : {result["content"]}")
    print(f"Summary : {result["summary"]}")
