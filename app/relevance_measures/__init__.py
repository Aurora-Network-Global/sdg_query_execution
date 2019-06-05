"""
The relevance measures Blueprint handles the creation and retrieval of relevance measures data
"""
from flask import Blueprint
relevance_measures_blueprint = Blueprint('relevance_measures', __name__, template_folder='templates')

from . import routes