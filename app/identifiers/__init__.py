"""
The eids Blueprint handles the creation and retrieval of EID lists
"""
from flask import Blueprint
identifiers_blueprint = Blueprint('identifiers', __name__, template_folder='templates')

from . import identifiers_routes
