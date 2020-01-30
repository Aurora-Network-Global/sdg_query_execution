"""
The eids Blueprint handles the creation and retrieval of EID lists
"""
from flask import Blueprint
analysis_blueprint = Blueprint('analysis', __name__, template_folder='templates')

from . import analysis_routes