from flask import Flask
from flask_cors import CORS

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_envvar("LIBINTEL_SETTINGS")
    CORS(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from app.eids import eids_blueprint
    from app.project import project_blueprint
    from app.relevance_measures import relevance_measures_blueprint
    from app.query import query_blueprint
    from app.scival import scival_blueprint
    from app.status import status_blueprint
    from app.collector import collector_blueprint
    from app.analysis import analysis_blueprint
    from app.keywords import keywords_blueprint

    app.register_blueprint(eids_blueprint, url_prefix='/eids')
    app.register_blueprint(project_blueprint, url_prefix='/project')
    app.register_blueprint(relevance_measures_blueprint)
    app.register_blueprint(scival_blueprint, url_prefix='/scival')
    app.register_blueprint(query_blueprint, url_prefix='/query')
    app.register_blueprint(status_blueprint, url_prefix='/status')
    app.register_blueprint(keywords_blueprint, url_prefix='/keywords')
    app.register_blueprint(analysis_blueprint)
    app.register_blueprint(collector_blueprint)
