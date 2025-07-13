from app_flask_langchain_rag_pipeline.extensions import mongo
from app_flask_langchain_rag_pipeline.logger_config import setup_logger

logger = setup_logger()


def create_account(account_data: dict):
    logger.info(f"Attempting to create account: {account_data['account_number']}")

    existing = mongo.db.account.find_one({"account_number": account_data["account_number"]})
    if existing:
        logger.warning(f"Account already exists: {account_data['account_number']}")
        return {"error": "Account already exists"}, 400

    mongo.db.account.insert_one(account_data)
    logger.info(f"Account created successfully: {account_data['account_number']}")
    return {"message": "Account created successfully", "account": account_data}, 201
