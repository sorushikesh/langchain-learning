from flask import request

from app_langgraph_fraud_detection.logger_config import setup_logger

logger = setup_logger()


def log_request_middleware(app):
    @app.before_request
    def log_request():
        body_data = {}
        try:
            body_data = request.get_json() if request.is_json else {}
        except Exception:
            pass

        logger.info(
            f"Incoming Request: {request.method} {request.path} | "
            f"IP: {request.remote_addr} | "
            f"Query: {request.args.to_dict()} | "
            f"Body: {body_data}"
        )
