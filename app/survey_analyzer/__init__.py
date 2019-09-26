from flask import Blueprint

survey_analyzer_blueprint = Blueprint('survey_analyzer', __name__, template_folder='templates')

from . import survey_analyzer_routes
