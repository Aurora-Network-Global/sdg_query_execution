import os

from flask import Flask
from flask_cors import CORS
import py_eureka_client.eureka_client as eureka_client


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)

    # read the environment parameter to retrieve the path to the configuration file
    if config_filename is None:
        app.config.from_envvar("LIBINTEL_SETTINGS")
    # check whether the query executor is part of a microservice architecture.
    # If it is, the configuration property 'EUREKA_URL' needs to be set.
    if app.config.get("EUREKA_URL") is not None:
        print('registering with eureka server', flush=True)
        server_url = app.config.get("EUREKA_URL")
        server_port = app.config.get("EUREKA_PORT")
        instance_port = int(os.environ.get("BIBLIOMETRICS_PORT", default=5000))
        eureka_client.init(eureka_server=server_url, app_name="query-executor",
                                           instance_port=instance_port)

    print('enabling CORS support', flush=True)
    # enable CORS support
    CORS(app)

    # register all blueprints
    print('registering blueprints', flush=True)
    register_blueprints(app)
    base_location = app.config.get("LIBINTEL_DATA_DIR")
    create_folders(base_location)

    return app


def create_folders(base_location):
    if not os.path.exists(base_location):
        os.makedirs(base_location)
    project_folder = base_location + '/out/'
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)


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
    from app.survey_analyzer import survey_analyzer_blueprint
    from app.crossref import crossref_blueprint
    from app.facettes import facettes_blueprint
    from app.wheel import wheel_blueprint
    from app.query_viewer import query_viewer_blueprint

    app.register_blueprint(eids_blueprint, url_prefix='/eids')
    app.register_blueprint(project_blueprint, url_prefix='/project')
    app.register_blueprint(relevance_measures_blueprint)
    app.register_blueprint(scival_blueprint, url_prefix='/scival')
    app.register_blueprint(query_blueprint, url_prefix='/query')
    app.register_blueprint(status_blueprint, url_prefix='/status')
    app.register_blueprint(keywords_blueprint, url_prefix='/keywords')
    app.register_blueprint(facettes_blueprint, url_prefix='/facettes')
    app.register_blueprint(survey_analyzer_blueprint, url_prefix='/survey_analyzer')
    app.register_blueprint(analysis_blueprint)
    app.register_blueprint(collector_blueprint)
    app.register_blueprint(crossref_blueprint, url_prefix='/crossref')
    app.register_blueprint(wheel_blueprint, url_prefix='/wheel')
    app.register_blueprint(query_viewer_blueprint, url_prefix='/viewer')

