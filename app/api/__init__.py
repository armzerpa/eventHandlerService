from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

# Import routes to register them with the blueprint
from app.api import events