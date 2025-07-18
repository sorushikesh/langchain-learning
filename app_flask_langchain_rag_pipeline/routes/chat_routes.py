from flask import Blueprint, request, jsonify
from app_flask_langchain_rag_pipeline.services.rag_service import query_rag

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    question = data.get("message")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    answer = query_rag(question)
    return jsonify({"answer": answer})