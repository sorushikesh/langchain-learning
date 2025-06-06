"""
Main class for playground
"""

from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from app.constants.config import ModelDetails
from app.constants.templates import Templates

information = """
"""

if __name__ == "__main__":

    variable = "information"
    information = ""

    summary_prompt_template = PromptTemplate(
        input_variables=[variable],
        template=Templates.summary_template
    )

    llm = AzureChatOpenAI(
        azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
        azure_endpoint=ModelDetails.AZURE_ENDPOINT,
        api_key=ModelDetails.AZURE_API_KEY,
        temperature=1,
        api_version=ModelDetails.AZURE_API_VERSION
    )

    chain = summary_prompt_template | llm
    response = chain.invoke(input={variable: information})

    print(response.content)
