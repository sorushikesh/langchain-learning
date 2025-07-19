from flask import Flask
from flask_cors import CORS

from app_langgraph_fraud_detection.config import Config
from app_langgraph_fraud_detection.extensions import mongo
from app_langgraph_fraud_detection.logger_config import setup_logger
from app_langgraph_fraud_detection.middlewares.request_logger import log_request_middleware

logger = setup_logger()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    mongo.init_app(app)

    log_request_middleware(app)

    return app


app = create_app()

if __name__ == "__main__":
    logger.info("Starting Fraud detection flask application...")
    app.run(host="0.0.0.0", port=8080, debug=True)
