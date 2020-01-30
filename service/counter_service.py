import json

from flask import current_app as app


def save_counter(project_id, counter, prefix=''):
    """saves the counter as json file on disk. a prefix can be given to distinguish different types of counter files"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/' + prefix + 'counter.json'
    with open(path_to_file, 'w') as json_file:
        json.dump(counter, json_file)
        json_file.close()


def load_counter(project_id, prefix=''):
    """retrieves a counter json file from disk. a prefix can be given to distinguish different types of counter files"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/' + prefix + 'counter.json'
    with open(path_to_file) as json_file:
        counter = json.load(json_file)
        json_file.close()
        return counter
