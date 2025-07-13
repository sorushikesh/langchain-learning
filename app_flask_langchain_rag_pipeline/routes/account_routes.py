from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app_flask_langchain_rag_pipeline.models.account_dto import AccountDTO
from app_flask_langchain_rag_pipeline.services.account_service import create_account

account_bp = Blueprint("account", __name__)

@account_bp.route("/accounts", methods=["POST"])
def add_account():
    try:
        account = AccountDTO(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    return create_account(account.dict())
