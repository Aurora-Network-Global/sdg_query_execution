import json

from flask import current_app as app


def load_status(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + query_id + '/status.json'
    with open(path_to_file) as json_file:
        status = json.load(json_file)
        json_file.close()
        return status


def save_status(query_id, status):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + query_id + '/status.json'
    with open(path_to_file, 'w') as json_file:
        json.dump(status.__dict__, json_file)
        json_file.close()
