import csv
import json
import os

from flask_cors import cross_origin

from SurveyGizmoSurvey.SurveyGizmoSurvey import SurveyGizmoSurvey
from SurveyGizmoSurvey.SurveyGizmoSurveyStats import SurveyGizmoSurveyStats
from app.survey_analyzer import survey_analyzer_blueprint

from flask import current_app as app, request, Response

from model.SurveyResult import SurveyResult
from service import facettes_service, survey_result_service
from service.eids_service import generate_judgement_file
from service.elasticsearch_service import HiddenEncoder


@cross_origin('localhost:4200')
@survey_analyzer_blueprint.route('/upload/<query_id>', methods=['POST'])
def upload_results_file(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    print("saving survey results file for " + query_id)
    if request.method == 'POST':
        file = request.files['survey-result-file']
        path_to_save = location + '/out/' + query_id + '/'
        print(path_to_save)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        file.save(path_to_save + 'survey_results.csv')
    return Response("OK", status=204)


@survey_analyzer_blueprint.route('/stats/<survey_id>', methods=['GET'])
def get_stats_for_survey(survey_id):
    print('collecting survey stats for survey id' + survey_id)
    survey_stats = SurveyGizmoSurveyStats(survey_id)
    print(survey_stats.cities_frequencies   )
    return json.dumps(survey_stats.cities_frequencies)



@survey_analyzer_blueprint.route('/import/<query_id>', methods=['GET'])
def import_survey_results_data(query_id):
    print('importing survey results')
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    with open(location + '/out/' + query_id + '/' + 'survey_results.csv', 'r', encoding='utf-8-sig') as csvfile:
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
                keywords_facettes = facettes_service.load_facettes_list(query_id)
                journal_facettes = facettes_service.load_facettes_list(query_id, 'journal')
            except:
                facettes_service.generate_lists(query_id)
                keywords_facettes = facettes_service.load_facettes_list(query_id)
                journal_facettes = facettes_service.load_facettes_list(query_id, 'journal')
            result.replace_keywords(keywords_facettes)
            result.replace_journals(journal_facettes)
            survey_results.append(result)
        csvfile.close()
        survey_result_service.save_survey_results(query_id, json.dumps(survey_results, cls=HiddenEncoder))
    return json.dumps(survey_results, cls=HiddenEncoder)


@survey_analyzer_blueprint.route('/collect/<query_id>', methods=['GET'])
def collect_survey_results_data(query_id):
    survey_id = request.args.get('survey_id')
    print('collecting survey results for survey id' + survey_id)
    survey = SurveyGizmoSurvey(survey_id)
    survey_results = survey.get_survey_results()
    judgements = []
    try:
        keywords_facettes = facettes_service.load_facettes_list(query_id)
        journal_facettes = facettes_service.load_facettes_list(query_id, 'journal')
    except:
        facettes_service.generate_lists(query_id)
        keywords_facettes = facettes_service.load_facettes_list(query_id)
        journal_facettes = facettes_service.load_facettes_list(query_id, 'journal')
    for result in survey_results:
        result.replace_keywords(keywords_facettes)
        result.replace_journals(journal_facettes)
        judgements = judgements + result.get_judgements()
    survey_result_service.save_survey_results(query_id, json.dumps(survey_results, cls=HiddenEncoder))
    generate_judgement_file(judgements, query_id)
    return json.dumps(survey_results, cls=HiddenEncoder)

