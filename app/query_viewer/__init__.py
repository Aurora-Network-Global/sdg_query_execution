"""
The query viewer Blueprint handles the display of stored xml queries
"""
from flask import Blueprint
query_viewer_blueprint = Blueprint('query_viewer', __name__, template_folder='templates')

from . import query_viewer_routes