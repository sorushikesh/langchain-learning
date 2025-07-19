from flask import request

from app_flask_langchain_rag_pipeline.logger_config import setup_logger

logger = setup_logger()


def log_request_middleware(app):
    @app.before_request
    def log_request():
        body_data = {}
        try:
            body_data = request.get_json() if request.is_json else {}
        except Exception as e:
            logger.exception("Exception occurred while parsing request body as JSON.")

        def sanitize_input(value):
            if isinstance(value, str):
                return value.replace('\n', '').replace('\r', '')
            if isinstance(value, dict):
                return {k: sanitize_input(v) for k, v in value.items()}
            if isinstance(value, list):
                return [sanitize_input(v) for v in value]
            return value  # For other types, return as is

        sanitized_method = sanitize_input(request.method)
        sanitized_path = sanitize_input(request.path)
        sanitized_query = sanitize_input(request.args.to_dict())
        sanitized_body = sanitize_input(body_data)

        logger.info(
            f"Incoming Request: {sanitized_method} {sanitized_path} | "
            f"IP: {request.remote_addr} | "
            f"Query: {sanitized_query} | "
            f"Body: {sanitized_body}"
        )
