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
            logger.warning(f"Failed to parse JSON from request body: {e}")

        def sanitize(value):
            if isinstance(value, str):
                return value.replace('\r', '').replace('\n', '')
            elif isinstance(value, dict):
                return {k: sanitize(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [sanitize(v) for v in value]
            return value

        sanitized_method = sanitize(request.method)
        sanitized_path = sanitize(request.path)
        sanitized_query = sanitize(request.args.to_dict())
        sanitized_body = sanitize(body_data)
        sanitized_ip = sanitize(request.remote_addr)

        logger.info(
            f"Incoming Request: {sanitized_method} {sanitized_path} | "
            f"IP: {sanitized_ip} | "
            f"Query: {sanitized_query} | "
            f"Body: {sanitized_body}"
        )
