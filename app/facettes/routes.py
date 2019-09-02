import os
import csv

from flask import Response, request, jsonify
from flask_cors import cross_origin

from . import facettes_blueprint
from flask import current_app as app


# uploads the test data and saves it as test_data.csv in the working directory
@facettes_blueprint.route('/journal/<query_id>', methods=['POST'])
def upload_journal_facettes_file(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    print("saving sample test file for " + query_id)
    file = request.files['journal-facettes']
    path_to_save = location + '/out/' + query_id + '/'
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    file.save(path_to_save + 'journal_facettes.csv')
    return Response('list saved', status=204)

# uploads the test data and saves it as test_data.csv in the working directory
@facettes_blueprint.route('/keyword/<query_id>', methods=['POST'])
def upload_keywords_facettes_file(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    print("saving sample test file for " + query_id)
    file = request.files['keyword-facettes']
    path_to_save = location + '/out/' + query_id + '/'
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    file.save(path_to_save + 'keywords_facettes.csv')
    return Response('list saved', status=204)


@cross_origin('*')
@facettes_blueprint.route('/keyword_list/<query_id>')
def retrieve_keyword_facettes_list(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    keyword_facettes = []
    with open(location + '/out/' + query_id + '/' + 'keywords_facettes.csv', 'r') as csvfile:
        linereader = csv.DictReader(csvfile, delimiter=',')
        for row in linereader:
            facette = {}
            if row.__len__() < 2:
                continue
            facette.keyword = row[0]
            facette.count = row[1]
            keyword_facettes.append(facette)
        csvfile.close()
    return jsonify(keyword_facettes)


@cross_origin('*')
@facettes_blueprint.route('/journal_list/<query_id>')
def retrieve_journal_facettes_list(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    journal_facettes = []
    with open(location + '/out/' + query_id + '/' + 'journal_facettes.csv', 'r') as csvfile:
        linereader = csv.DictReader(csvfile, delimiter=',')
        for row in linereader:
            if row.__len__() < 2:
                continue
            print(row['count'])
            journal_facettes.append({
                'journal': row['journal'],
                'count': int(row['count'])
            })
        csvfile.close()
    return jsonify(journal_facettes)
