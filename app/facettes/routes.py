import os
import csv

from flask import Response, request, jsonify
from flask_cors import cross_origin

from service import facettes_service
from . import facettes_blueprint
from flask import current_app as app


# uploads the test data and saves it as test_data.csv in the working directory
@facettes_blueprint.route('/upload/<query_id>', methods=['POST'])
def upload_facettes_file(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    print("saving facettes file for " + query_id)
    file = request.files['facettes']
    path_to_save = location + '/out/' + query_id + '/'
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    file.save(path_to_save + 'facettes.csv')
    return Response('facettes saved', status=204)


@cross_origin('*')
@facettes_blueprint.route('/journal_list/<query_id>')
def retrieve_journal_facettes_list(query_id):
    sample_size = int(request.args.get('sample_size'))
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    journal_facettes = []
    with open(location + '/out/' + query_id + '/' + 'facettes.csv', 'r', encoding='utf-8-sig') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')
        for row in linereader:
            if row.__len__() < 16:
                continue
            # skip header line
            if row[12] == 'SOURCE TITLE':
                continue
            # skip empty data
            if row[12] == '':
                continue
            if row[13] == '':
                continue

            journal_facettes.append({
                'journal': row[12],
                'count': int(row[13])
            })
        csvfile.close()
    with open(location + '/out/' + query_id + '/' + 'journal_facettes.txt', 'w', encoding='utf-8') as facettes_file:
        for journal_facette in journal_facettes:
            facettes_file.write(journal_facette['journal'] + '\n')
        facettes_file.close()
    return jsonify(journal_facettes[:sample_size])


@facettes_blueprint.route('/generate_lists/<query_id>', methods=['POST'])
def generate_lists(query_id):
    facettes_service.generate_lists(query_id);
    return Response('list files generated', status=204)


@cross_origin('*')
@facettes_blueprint.route('/keyword_list/<query_id>')
def retrieve_keyword_facettes_list(query_id):
    sample_size = int(request.args.get('sample_size'))
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    keyword_facettes = []
    with open(location + '/out/' + query_id + '/' + 'facettes.csv', 'r', encoding='utf-8-sig') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')
        for row in linereader:
            # skip first lines
            if row.__len__() < 16:
                continue
            # skip header line
            if row[14] == 'KEYWORD':
                continue

            # skip empty data
            if row[14] == '':
                continue
            if row[15] == '':
                continue
            keyword_facettes.append({
                'keyword': row[14],
                'count': int(row[15])
            })
        csvfile.close()
    with open(location + '/out/' + query_id + '/' + 'keyword_facettes.txt', 'w', encoding='utf-8') as facettes_file:
        for keyword_facette in keyword_facettes:
            facettes_file.write(keyword_facette['keyword'] + '\n')
        facettes_file.close()
    return jsonify(keyword_facettes[:sample_size])
