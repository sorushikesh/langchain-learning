from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA
from langchain_core.documents import Document

from app.constants.config import ModelDetails
from app_flask_langchain_rag_pipeline.constants.templates import PromptTemplates
from app_flask_langchain_rag_pipeline.extensions import mongo
from app_flask_langchain_rag_pipeline.logger_config import setup_logger
from app_flask_langchain_rag_pipeline.config import Config

logger = setup_logger()

_embeddings = None
_vector_store = None

PROMPT = PromptTemplate(
    template=PromptTemplates.SYSTEM_PROMPT,
    input_variables=["context", "question"]
)


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        logger.debug("Initializing HuggingFace embeddings model")
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings


def _get_vector_store():
    """Setting up mongoDB atlas vector store"""
    global _vector_store
    if _vector_store is None:
        logger.debug("Setting up MongoDB Atlas vector store")
        client = mongo.cx
        collection = client[Config.DB_NAME][Config.VECTOR_COLLECTION]
        _vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=_get_embeddings(),
            index_name="vector_index",
            text_key="text",
        )
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
    logger.debug("Running RAG pipeline for question: %s", question)
    result = build_qa_chain().invoke({"query": question})
    return result.get("result", "")

def build_qa_chain():
    retriever = _get_vector_store().as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5}
    )

    llm = ChatAnthropic(
        model_name=ModelDetails.ANTHROPIC_MODEL_ID,
        max_tokens_to_sample=ModelDetails.MAX_TOKENS,
        temperature=ModelDetails.TEMPERATURE,
        api_key=ModelDetails.ANTHROPIC_API_KEY,
        timeout=None,
        stop=None
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )