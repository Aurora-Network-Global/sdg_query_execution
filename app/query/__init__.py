"""
The query Blueprint handles the creation and retrieval of query objects and database specific query strings
"""
from flask import Blueprint
query_blueprint = Blueprint('query', __name__, template_folder='templates')

from . import query_routes
