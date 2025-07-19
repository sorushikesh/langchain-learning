import logging

from langchain.schema import AIMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from app_langchain_anthropic.anthropic_claude import call_claude, stream_claude_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_history: BaseChatMessageHistory = ChatMessageHistory()


def generate_response(message: str) -> str:
    logger.info("Received user message: %s", message)

    chat_history.add_user_message(HumanMessage(content=message))
    logger.debug("Updated chat history with user message.")

    history_text = "\n".join(
        f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages
    )
    logger.debug("Compiled chat history for model input:\n%s", history_text)

    try:
        response = call_claude(history_text)
        logger.info("Received response from Claude.")
    except Exception as e:
        logger.exception("Error while calling Claude model: %s", e)
        return "An error occurred while generating a response."

    chat_history.add_ai_message(AIMessage(content=response))
    logger.debug("Updated chat history with AI response.")

    logger.info("Returning response to user.")
    return response


def stream_generate_response(message: str):
    logger.info("Received user message: %s", message)

    chat_history.add_user_message(HumanMessage(content=message))
    logger.debug("Updated chat history with user message.")

    history_text = "\n".join(
        f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages
    )
    logger.debug("Compiled chat history for model input:\n%s", history_text)

    ai_response_buffer = ""

    try:
        for token in stream_claude_response(history_text):
            ai_response_buffer += token
            yield token

        chat_history.add_ai_message(AIMessage(content=ai_response_buffer))
        logger.debug("Updated chat history with streamed AI response.")

        logger.info("Completed streaming response to user.")
    except Exception as e:
        logger.exception("Streaming Claude call failed: %s", e)
        yield "[ERROR] Claude failed to generate a response."
