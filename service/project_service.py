import json
import os

from flask import current_app as app


def load_project(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '.json'
    with open(path_to_file) as json_file:
        project = json.load(json_file)
        json_file.close()
        return project


def save_project(project):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    json_string = json.dumps(project)
    out_dir = location + '/out/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + project['project_id'] + '.json', 'w') as json_file:
        json_file.write(json_string)

