from flask import Flask
from flask_pymongo import PyMongo
from config import config

# Initialize MongoDB extension
mongo = PyMongo()

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize MongoDB with the Flask app
    # We need to explicitly set MONGO_URI since it's a property in the config class
    app.config['MONGO_URI'] = config[config_name]().MONGO_URI
    mongo.init_app(app)

    # Register blueprints
    from app.api import api_blueprint
    app.register_blueprint(api_blueprint)

    return app