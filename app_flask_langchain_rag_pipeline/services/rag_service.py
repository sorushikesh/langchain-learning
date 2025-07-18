from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA
from langchain_core.documents import Document

from app.constants.config import ModelDetails
from app_flask_langchain_rag_pipeline.extensions import mongo
from app_flask_langchain_rag_pipeline.logger_config import setup_logger
from app_flask_langchain_rag_pipeline.config import Config

logger = setup_logger()

_embeddings = None
_vector_store = None


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        logger.debug("Initializing HuggingFace embeddings model")
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings


def _get_vector_store():
    global _vector_store
    if _vector_store is None:
        logger.debug("Setting up MongoDB Atlas vector store")
        client = mongo.cx
        collection = client[Config.DB_NAME][Config.VECTOR_COLLECTION]
        _vector_store = MongoDBAtlasVectorSearch(collection, _get_embeddings())
    return _vector_store


def store_transaction_embedding(transaction: dict):
    """Store transaction details in the vector store for later retrieval."""
    vs = _get_vector_store()
    text = (
        f"{transaction['transaction_type']} transaction of "
        f"{transaction['transaction_amount']} on {transaction['transaction_date']} "
        f"for account {transaction['account_number']} - {transaction.get('description', '')}"
    )
    doc = Document(
        page_content=text, metadata={"account_number": transaction["account_number"]}
    )
    logger.debug("Adding transaction document to vector store: %s", text)
    vs.add_documents([doc])


def query_rag(question: str) -> str:
    """Query the vector store and generate an answer using a language model."""
    vs = _get_vector_store()
    retriever = vs.as_retriever()
    llm = ChatAnthropic(
        model_name=ModelDetails.ANTHROPIC_MODEL_ID,
        max_tokens_to_sample=ModelDetails.MAX_TOKENS,
        temperature=ModelDetails.TEMPERATURE,
        api_key=ModelDetails.ANTHROPIC_API_KEY,
        timeout=None,
        stop=None
    )
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
    logger.debug("Running RAG pipeline for question: %s", question)
    result = qa_chain.invoke({"query": question})
    return result.get("result", "")