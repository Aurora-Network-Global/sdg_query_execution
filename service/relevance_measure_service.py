import json
from json import JSONDecodeError

from flask import current_app as app

from model.RelevanceMeasures import RelevanceMeasure


def save_relevance_measures(project_id, relevance_measures):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/relevance_measures.json'
    with open(path_to_file, 'w') as json_file:
        json_file.write(json.dumps(relevance_measures))
        json_file.close()


def load_relevance_measure(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/relevance_measures.json'
    with open(path_to_file) as json_file:
        try:
            relevance_measure = json.load(json_file)
            json_file.close()
            return relevance_measure
        except FileNotFoundError:
            return {}
        except JSONDecodeError:
            return {}

