from flask import request

from app_langgraph_fraud_detection.logger_config import setup_logger

logger = setup_logger()


def log_request_middleware(app):
    @app.before_request
    def log_request():
        body_data = {}
        try:
            body_data = request.get_json() if request.is_json else {}
            # Sanitize body data to remove newline characters
            body_data = {k: str(v).replace('\r\n', '').replace('\n', '') for k, v in body_data.items()}
        except Exception as e:
            logger.error(f"Failed to parse request body: {e}")

        # Sanitize query parameters to remove newline characters
        sanitized_query = {k: str(v).replace('\r\n', '').replace('\n', '') for k, v in request.args.to_dict().items()}

        sanitized_method = str(request.method).replace('\r\n', '').replace('\n', '')
        sanitized_path = str(request.path).replace('\r\n', '').replace('\n', '')
        sanitized_ip = str(request.remote_addr).replace('\r\n', '').replace('\n', '')
        
        logger.info(
            f"Incoming Request: {sanitized_method} {sanitized_path} | "
            f"IP: {sanitized_ip} | "
            f"Query: {sanitized_query} | "
            f"Body: {body_data}"
        )
