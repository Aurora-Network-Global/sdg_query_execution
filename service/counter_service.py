import json

from flask import current_app as app


def save_counter(project_id, counter, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/' + prefix + 'counter.json'
    with open(path_to_file, 'w') as json_file:
        json.dump(counter, json_file)
        json_file.close()


def load_counter(project_id, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/' + prefix + 'counter.json'
    with open(path_to_file) as json_file:
        counter = json.load(json_file)
        json_file.close()
        return counter
