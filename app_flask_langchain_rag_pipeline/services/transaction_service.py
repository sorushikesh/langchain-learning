from app_flask_langchain_rag_pipeline.extensions import mongo
from app_flask_langchain_rag_pipeline.logger_config import setup_logger

logger = setup_logger()

def process_transaction(transaction_data: dict):
    account_number = transaction_data["account_number"]
    logger.info(f"Processing transaction for account: {account_number}")

    account = mongo.db.account.find_one({"account_number": account_number})
    if not account:
        logger.error(f"Account not found: {account_number}")
        return {"error": "Account not found"}, 404

    current_balance = account.get("current_balance", 0.0)
    txn_type = transaction_data["transaction_type"].lower()
    amount = transaction_data["transaction_amount"]

    if txn_type == "debit":
        if amount > current_balance:
            logger.warning(f"Insufficient funds for account {account_number}. Requested: {amount}, Available: {current_balance}")
            return {"error": "Insufficient balance"}, 400
        new_balance = current_balance - amount
    elif txn_type == "credit":
        new_balance = current_balance + amount
    else:
        logger.error(f"Invalid transaction type: {txn_type}")
        return {"error": "Invalid transaction type"}, 400

    mongo.db.account.update_one(
        {"account_number": account_number},
        {"$set": {"current_balance": new_balance}}
    )
    mongo.db.transaction.insert_one(transaction_data)

    logger.info(f"Transaction processed for account {account_number}. New balance: {new_balance}")
    return {"message": "Transaction successful", "new_balance": new_balance}, 200
