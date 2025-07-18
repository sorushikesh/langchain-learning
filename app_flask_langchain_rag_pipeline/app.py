from flask import Flask
from flask_cors import CORS

from app_flask_langchain_rag_pipeline.config import Config
from app_flask_langchain_rag_pipeline.extensions import mongo
from app_flask_langchain_rag_pipeline.routes.account_routes import account_bp
from app_flask_langchain_rag_pipeline.routes.chat_routes import chat_bp
from app_flask_langchain_rag_pipeline.routes.transaction_routes import transaction_bp
from app_flask_langchain_rag_pipeline.logger_config import setup_logger
from app_flask_langchain_rag_pipeline.middlewares.request_logger import (
    log_request_middleware,
)
logger = setup_logger()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    mongo.init_app(app)

    log_request_middleware(app)

    app.register_blueprint(account_bp, url_prefix="/api")
    app.register_blueprint(transaction_bp, url_prefix="/api")
    app.register_blueprint(chat_bp, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask Invoice Management API...")
    app.run(host="0.0.0.0", port=8080, debug=True)
