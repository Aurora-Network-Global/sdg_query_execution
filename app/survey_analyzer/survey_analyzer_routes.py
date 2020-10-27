################
#    imports   #
################

import json
import os

from flask_cors import cross_origin

from app.survey_analyzer import survey_analyzer_blueprint

from flask import current_app as app, request, Response

from service import survey_service, elasticsearch_service, project_service
from service.elasticsearch_service import HiddenEncoder


################
#    routes    #
################

@cross_origin('localhost:4200')
@survey_analyzer_blueprint.route('/upload/<project_id>', methods=['POST'])
def upload_results_file(project_id):
    """
    retrieves a file from the request and saves it as survey_results.csv to disc
    :param project_id:
    :return:
    """
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    app.logger.info("project {}: saving survey results file for ".format(project_id))
    if request.method == 'POST':
        file = request.files['survey-result-file']
        path_to_save = location + '/out/' + project_id + '/'
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        file.save(path_to_save + 'survey_results.csv')
    return Response("OK", status=204)


@survey_analyzer_blueprint.route('/setSurveyId/<project_id>', methods=['POST'])
def set_survey_id(project_id):
    survey_id = request.form['survey_id']
    project = project_service.load_project(project_id)
    project.survey_id = survey_id
    project_service.save_project(project)
    app.logger.info('project {}: connecting with survey {}'.format(project_id, survey_id))
    return Response('survey ID saved', status=204)


@survey_analyzer_blueprint.route('/collect/<project_id>', methods=['GET'])
def collect_survey_results_data(project_id):
    """
    queries the SurveyGizmo API to collect the data for a given survey
    :param project_id: the ID of the current project
    :return: a JSON formatted list of SurveyGizmo survey results
    """
    project = project_service.load_project(project_id)
    survey = survey_service.collect_survey_data(project)
    survey_service.save_survey(survey)
    elasticsearch_service.delete_survey_index(survey)
    elasticsearch_service.save_survey(survey)
    app.logger.info('project {}: collecting survey data'.format(project_id))
    return Response(json.dumps(survey.survey_results, cls=HiddenEncoder), status=200)


@survey_analyzer_blueprint.route('/load/<project_id>', methods=['GET'])
def load_survey_results_data(project_id):
    """
    loads the survey data from disc.
    :param project_id: the ID of the current project
    :return: a JSON formatted list of survey results
    """
    survey = survey_service.load_survey(project_id)
    return Response(json.dumps(survey.survey_results, default=lambda o: o.__getstate__()), status=200)
