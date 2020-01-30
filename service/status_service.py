import json

from flask import current_app as app

from model.Status import Status


def load_status(project_id):
    """loads the status from disc"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/status.json'
    with open(path_to_file) as json_file:
        status = json.load(json_file)
        json_file.close()
        return Status(**status)


def save_status(project_id, status):
    """saves the status object as json file on disc"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/status.json'
    with open(path_to_file, 'w') as json_file:
        json_file.write(json.dumps(status, default=lambda o: o.__getstate__()))
        json_file.close()
