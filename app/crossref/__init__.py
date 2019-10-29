from flask import Blueprint

crossref_blueprint = Blueprint('crossref', __name__, template_folder='templates')

from . import crossref_routes