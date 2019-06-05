"""
The project Blueprint handles the creation and retrieval of project files
"""
from flask import Blueprint
project_blueprint = Blueprint('project', __name__, template_folder='templates')

from . import routes
