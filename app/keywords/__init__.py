"""
The eids Blueprint handles the creation and retrieval of EID lists
"""
from flask import Blueprint
keywords_blueprint = Blueprint('keywords', __name__, template_folder='keywords')

from . import routes
