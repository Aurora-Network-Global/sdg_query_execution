"""
The query Blueprint handles the creation and retrieval of query objects and database specific query strings
"""
from flask import Blueprint

scival_blueprint = Blueprint('scival', __name__, template_folder='templates')

from . import routes
