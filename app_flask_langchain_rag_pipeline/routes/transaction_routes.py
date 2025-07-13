from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app_flask_langchain_rag_pipeline.models.transaction_dto import TransactionDTO
from app_flask_langchain_rag_pipeline.services.transaction_service import process_transaction

transaction_bp = Blueprint("transaction", __name__)

@transaction_bp.route("/transactions", methods=["POST"])
def add_transaction():
    try:
        txn = TransactionDTO(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    return process_transaction(txn.dict())
