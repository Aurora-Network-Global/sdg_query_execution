"""
The eids Blueprint handles the creation and retrieval of EID lists
"""
from flask import Blueprint
eids_blueprint = Blueprint('eids', __name__, template_folder='templates')

from . import routes
