"""
The wheel Blueprint handles the creation and retrieval of sdg wheel depiction
"""
from flask import Blueprint
wheel_blueprint = Blueprint('wheel', __name__, template_folder='templates')

from . import wheel_routes
