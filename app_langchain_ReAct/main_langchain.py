import langchain_anthropic
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType

from app_langchain_ReAct.config import ModelDetails
from app_langchain_ReAct.tools import tools

llm = langchain_anthropic.ChatAnthropic(
    model_name=ModelDetails.ANTHROPIC_MODEL_ID,
    max_tokens_to_sample=ModelDetails.MAX_TOKENS,
    temperature=ModelDetails.TEMPERATURE,
    timeout=None,
    stop=None
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

print(agent.invoke(
    "I'm in Canada and I have 10000 CAD. My wife, who is from India, wants to buy a house in Cape Town, South Africa, for 1,000,000 in the local currency. She has 24% of the total cost. Can I help her with this purchase if we take loan for 5 years. how much EMI I have to pay ?"))
