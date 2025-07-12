import logging
from anthropic import Anthropic
from anthropic.types import MessageParam

from app.constants.config import ModelDetails
from app.constants.templates import prompt_loader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = ModelDetails.ANTHROPIC_API_KEY
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")

client = Anthropic(api_key=API_KEY)


def call_claude(prompt: str) -> str:
    logger.info("Preparing request for Claude model (Anthropic API).")

    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    try:
        response = client.messages.create(
            model=ModelDetails.ANTHROPIC_MODEL_ID,
            max_tokens=ModelDetails.MAX_TOKENS,
            temperature=ModelDetails.TEMPERATURE,
            system=prompt_loader.get_system_prompt(),
            messages=messages,
        )
        logger.info("Successfully received response from Claude.")

        return "".join(block.text for block in response.content)

    except Exception as e:
        logger.exception("Error while calling Claude model: %s", e)
        raise
