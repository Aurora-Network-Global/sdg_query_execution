"""
The status Blueprint handles the retrieval of status objects
"""
from flask import Blueprint

status_blueprint = Blueprint('status', __name__, template_folder='status')

from . import status_routes
