from flask import Blueprint
facettes_blueprint = Blueprint('facettes', __name__, template_folder='templates')

from . import facettes_routes
