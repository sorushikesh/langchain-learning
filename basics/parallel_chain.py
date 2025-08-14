from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import AzureChatOpenAI

from app.constants.config import ModelDetails

llm = AzureChatOpenAI(
    azure_endpoint=ModelDetails.AZURE_ENDPOINT,
    azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
    api_key=ModelDetails.AZURE_API_KEY,
    api_version=ModelDetails.AZURE_API_VERSION,
    temperature=1
)

summary_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a short summary about {topic}."
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary")

points_prompt = PromptTemplate(
    input_variables=["topic"],
    template="List 5 key points about {topic}."
)
points_chain = LLMChain(llm=llm, prompt=points_prompt, output_key="key_points")

tweet_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a tweet (max 280 characters) about {topic}."
)
tweet_chain = LLMChain(llm=llm, prompt=tweet_prompt, output_key="tweet")

parallel_chain = RunnableParallel(
    summary=summary_chain,
    key_points=points_chain,
    tweet=tweet_chain
)

if __name__ == "__main__":
    topic = "artificial intelligence in healthcare"
    results = parallel_chain.invoke({"topic": topic})

    print("\n=== Summary ===")
    print(results["summary"])
    print("\n=== Key Points ===")
    print(results["key_points"])
    print("\n=== Tweet ===")
    print(results["tweet"])