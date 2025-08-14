from app.util.config import ModelDetails
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=ModelDetails.AZURE_ENDPOINT,
    azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
    api_key=ModelDetails.AZURE_API_KEY,
    api_version=ModelDetails.AZURE_API_VERSION,
    temperature=1
)

# Router
router_prompt = PromptTemplate(
    input_variables=["query"],
    template=
    """
    You are a support query classifier.
    Classify the following customer query into exactly one category:
    - technical (if about bugs, errors, crashes, problems)
    - billing (if about invoices, payments, refunds, charges)
    - default (if none of the above)
    
    Query: {query}
    Category:
    """
)
router_chain = LLMChain(llm=llm, prompt=router_prompt, output_key="category")

technical_prompt = PromptTemplate(
    input_variables=["query"],
    template="You are a technical support engineer. Answer the technical issue in detail: {query}"
)
technical_chain = LLMChain(llm=llm, prompt=technical_prompt)

billing_prompt = PromptTemplate(
    input_variables=["query"],
    template="You are a billing support agent. Answer the billing question in detail: {query}"
)
billing_chain = LLMChain(llm=llm, prompt=billing_prompt)

default_prompt = PromptTemplate(
    input_variables=["query"],
    template="You are a friendly customer support assistant. Answer this question: {query}"
)
default_chain = LLMChain(llm=llm, prompt=default_prompt)

destination_chains = {
    "technical": technical_chain,
    "billing": billing_chain,
    "default": default_chain
}

if __name__ == "__main__":
    query = "I was charged twice for my subscription"

    category_result = router_chain.invoke({"query": query})
    category = category_result["category"].strip().lower()
    chosen_chain = destination_chains.get(category, default_chain)

    print(f"User Query: {query}")
    print(f"AI Routed to: {category} support\n")
    response = chosen_chain.run({"query": query})
    print(response)
