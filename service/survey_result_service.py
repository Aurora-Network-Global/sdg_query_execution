import json
import os

from flask import current_app as app


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
