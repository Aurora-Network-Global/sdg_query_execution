import json

from flask import current_app as app


def save_relevance_measures(project_id, relevance_measures):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/relevance_measures.json'
    with open(path_to_file, 'w') as json_file:
        json_file.write(json.dumps(relevance_measures.__dict__))
        json_file.close()


def load_relevance_measure(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/relevance_measures.json'
    print(path_to_file)
    with open(path_to_file) as json_file:
        relevance_measure = json.load(json_file)
        print(relevance_measure)
        json_file.close()
        return relevance_measure
