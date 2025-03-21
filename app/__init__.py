from flask import Flask
from config import config


def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    from app.api import api_blueprint
    app.register_blueprint(api_blueprint)

    return app