import json
import os

from flask import current_app as app
from utilities import utils


def load_query(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/query.json'
    with open(path_to_file) as json_file:
        query = json.load(json_file)
        json_file.close()
        return query


def save_query(project_id, query):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    json_string = json.dumps(query)
    out_dir = location + '/out/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + project_id + '.json', 'w') as json_file:
        json_file.write(json_string)


def save_scopus_query(project_id, query):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    # convert the JSON search object to the search string for the scopus api
    search_string = utils.convert_search_to_scopus_search_string(query)
    path_to_file = location + '/out/' + project_id + '/scopus_search_string.txt'
    with open(path_to_file, 'w') as scopus_search_string_file:
        scopus_search_string_file.write(search_string)
        scopus_search_string_file.close()


def load_scopus_query(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/scopus_search_string.txt'
    with open(path_to_file) as json_file:
        search_string = json_file.read()
        json_file.close()
        return search_string