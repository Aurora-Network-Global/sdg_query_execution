################
#    imports   #
################

import csv
import json
import os

from flask_cors import cross_origin

from SurveyGizmoSurvey.SurveyGizmoSurvey import SurveyGizmoSurvey
from SurveyGizmoSurvey.SurveyGizmoSurveyStats import SurveyGizmoSurveyStats
from app.survey_analyzer import survey_analyzer_blueprint

from flask import current_app as app, request, Response
from pybliometrics import scopus

from model.AllResponses import AllResponses
from model.SurveyResult import SurveyResult
from service import facettes_service, survey_result_service, elasticsearch_service, project_service
from service.eids_service import generate_judgement_file
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
        survey_result_service.save_survey_results(project_id, json.dumps(survey_results, cls=HiddenEncoder))
    return json.dumps(survey_results, cls=HiddenEncoder)


@survey_analyzer_blueprint.route('/collect/<project_id>', methods=['GET'])
def collect_survey_results_data(project_id):
    """
    queries the SurveyGizmo API to collect the data for a given survey
    :param project_id: the ID of the current project
    :return: a JSON formatted list of SurveyGizmo survey results
    """
    survey_id = request.args.get('survey_id')
    project = project_service.load_project(project_id)
    print('collecting survey results for survey id {}'.format(survey_id))
    survey = SurveyGizmoSurvey(survey_id)
    survey_results = survey.get_survey_results()
    judgements = []
    try:
        keywords_facettes = facettes_service.load_facettes_list(project_id)
        journal_facettes = facettes_service.load_facettes_list(project_id, 'journal')
    except:
        facettes_service.generate_lists(project_id)
        keywords_facettes = facettes_service.load_facettes_list(project_id)
        journal_facettes = facettes_service.load_facettes_list(project_id, 'journal')
    for result in survey_results:
        result.replace_keywords(keywords_facettes)
        result.replace_journals(journal_facettes)
        judgements = judgements + result.get_judgements()
    for judgement in judgements:
        scopus_abstract = scopus.AbstractRetrieval(judgement['eid'], view="FULL")
        response = AllResponses(judgement['eid'], project.name, project.project_id)
        response.scopus_abstract_retrieval = scopus_abstract
        response.accepted = judgement['judgement']
        elasticsearch_service.send_to_index(response, project_id)
    survey_result_service.save_survey_results(project_id, json.dumps(survey_results, cls=HiddenEncoder))
    generate_judgement_file(judgements, project_id)
    return json.dumps(survey_results, cls=HiddenEncoder)

