import json
import os

from flask import current_app as app
from pybliometrics import scopus

from SurveyGizmoSurvey.SurveyGizmoSurvey import SurveyGizmoSurvey
from model.AllResponses import AllResponses
from service import facettes_service
from service.eids_service import generate_judgement_file
from utilities.HiddenEncoder import HiddenEncoder
from utilities.utils import replace_index_by_clear_name


def load_survey_results(project_id, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/' + prefix + 'survey_result.json'
    with open(path_to_file) as json_file:
        result = json.load(json_file)
        json_file.close()
    return result


def load_survey_results_as_string(project_id, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/' + prefix + 'survey_result.json'
    with open(path_to_file) as json_file:
        return json_file.readlines()


def save_survey_results(project_id, json_string, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    out_dir = location + '/out/' + project_id
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + '/' + prefix + 'survey_result.json', 'w') as json_file:
        json_file.write(json_string)


def save_survey(survey, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    out_dir = location + '/out/' + survey.project_id
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + '/' + prefix + 'survey.json', 'w') as json_file:
        json_file.write(json.dumps(survey, cls=HiddenEncoder))


def collect_survey_data(project):
    print('collecting survey results for survey id {}'.format(project.survey_id))
    gizmo_survey = SurveyGizmoSurvey(survey_id=project.survey_id, project_id=project.project_id)
    survey_results = gizmo_survey.survey.survey_results
    judgements = []
    try:
        keywords_facettes = facettes_service.load_facettes_list(project.project_id)
        journals_facettes = facettes_service.load_facettes_list(project.project_id, 'journal')
    except:
        facettes_service.generate_lists(project.project_id)
        keywords_facettes = facettes_service.load_facettes_list(project.project_id)
        journals_facettes = facettes_service.load_facettes_list(project.project_id, 'journal')
    for result in survey_results:
        replace_index_by_clear_name(result.selected_keywords, keywords_facettes)
        replace_index_by_clear_name(result.unselected_keywords, keywords_facettes)
        replace_index_by_clear_name(result.selected_journals, journals_facettes)
        replace_index_by_clear_name(result.unselected_journals, journals_facettes)
        judgements = judgements + result.judgements
    for judgement in judgements:
        scopus_abstract = scopus.AbstractRetrieval(judgement['eid'], view="FULL")
        response = AllResponses(judgement['eid'], project.name, project.project_id)
        response.scopus_abstract_retrieval = scopus_abstract
        response.accepted = judgement['judgement']
        # elasticsearch_service.send_to_index(response, project_id)
    generate_judgement_file(judgements, project.project_id)
    return gizmo_survey.survey

