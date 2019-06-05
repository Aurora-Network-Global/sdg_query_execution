"""
The eids Blueprint handles the creation and retrieval of EID lists
"""
from flask import Blueprint
collector_blueprint = Blueprint('collector', __name__, template_folder='templates')

from . import routes
