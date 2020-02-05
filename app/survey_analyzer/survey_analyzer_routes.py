################
#    imports   #
################

import csv
import json
import os

from flask_cors import cross_origin

from SurveyGizmoSurvey.SurveyGizmoSurveyStats import SurveyGizmoSurveyStats
from app.survey_analyzer import survey_analyzer_blueprint

from flask import current_app as app, request, Response
from pybliometrics import scopus

from model.AllResponses import AllResponses
from model.SurveyResult import SurveyResult
from service import facettes_service, survey_service, elasticsearch_service, project_service
from service.elasticsearch_service import HiddenEncoder


################
#    routes    #
################
from service.survey_service import collect_survey_data
from utilities.utils import replace_index_by_clear_name


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
    print("saving survey results file for " + project_id)
    if request.method == 'POST':
        file = request.files['survey-result-file']
        path_to_save = location + '/out/' + project_id + '/'
        print(path_to_save)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        file.save(path_to_save + 'survey_results.csv')
    return Response("OK", status=204)


@survey_analyzer_blueprint.route('/stats/<survey_id>', methods=['GET'])
def get_stats_for_survey(survey_id):
    """
    returns the general statistics for the survey.
    :param survey_id: the ID of the survey
    :return: a JSON formatted SurveyStats object
    """
    print('collecting survey stats for survey id' + survey_id)
    survey_stats = SurveyGizmoSurveyStats(survey_id)
    print(survey_stats.cities_frequencies   )
    return json.dumps(survey_stats.cities_frequencies)


@survey_analyzer_blueprint.route('/import/<project_id>', methods=['GET'])
def import_survey_results_data(project_id):
    """
    imports the survey responses from the survey_results.csv file
    :param project_id: the ID of the current project
    :return: a JSON formatted SurveyResult object
    """
    print('importing survey results')
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    with open(location + '/out/' + project_id + '/' + 'survey_results.csv', 'r', encoding='utf-8-sig') as csvfile:
        survey_results = []
        linereader = csv.reader(csvfile, delimiter=',')
        for row in linereader:
            if row.__len__() < 10:
                continue
            if 'Response ID' in row[0]:
                continue
            if row[3] == 'Partial':
                continue
            if 'test' in row[9]:
                continue
            result = SurveyResult(row)
            try:
                keywords_facettes = facettes_service.load_facettes_list(project_id)
                journal_facettes = facettes_service.load_facettes_list(project_id, 'journal')
            except:
                facettes_service.generate_lists(project_id)
                keywords_facettes = facettes_service.load_facettes_list(project_id)
                journal_facettes = facettes_service.load_facettes_list(project_id, 'journal')
            result.replace_keywords(keywords_facettes)
            result.replace_journals(journal_facettes)
            survey_results.append(result)
        csvfile.close()
        survey_service.save_survey_results(project_id, json.dumps(survey_results, cls=HiddenEncoder))
    return json.dumps(survey_results, cls=HiddenEncoder)


@survey_analyzer_blueprint.route('/setSurveyId/<project_id>', methods=['POST'])
def set_survey_id(project_id):
    survey_id = request.form['survey_id']
    project = project_service.load_project(project_id)
    project.survey_id = survey_id
    project_service.save_project(project)
    print('connecting project {} with survey {}'.format(project_id, survey_id))
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
    elasticsearch_service.save_survey(survey)
    return Response(json.dumps(survey.survey_results, cls=HiddenEncoder), status=200)

@survey_analyzer_blueprint.route('/load/<project_id>', methods=['GET'])
def load_survey_results_data(project_id):
    """
    loads the survey data from disc.
    :param project_id: the ID of the current project
    :return: a JSON formatted list of survey results
    """
    survey_results = survey_service.load_survey_results(project_id)
    return Response(json.dumps(survey_results, cls=HiddenEncoder), status=200)
