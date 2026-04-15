import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.config import config
from app.extensions import db, bcrypt, jwt, migrate, cors


def create_app(config_name=None):
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialise extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register blueprints (inside factory!)
    from app.routes import (
        auth_bp, profile_bp, projects_bp, comments_bp,
        likes_bp, collaborations_bp, milestones_bp
    )
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(likes_bp)
    app.register_blueprint(collaborations_bp)
    app.register_blueprint(milestones_bp)

    # Register error handlers
    register_error_handlers(app)

    # Setup logging for production
    if not app.debug and not app.testing:
        setup_logging(app)

    # Simple health check endpoint
    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app


def register_error_handlers(app):
    """Global error handling."""
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        app.logger.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


def setup_logging(app):
    """Configure file logging for production."""
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/mzansibuilds.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("MzansiBuilds startup")