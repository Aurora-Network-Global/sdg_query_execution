#################
#    imports    #
#################

import os
import csv

from flask import Response, request, jsonify
from flask_cors import cross_origin

from service import facettes_service
from . import facettes_blueprint
from flask import current_app as app


#################
#    routes     #
#################

@facettes_blueprint.route('/upload/<project_id>', methods=['POST'])
def upload_facettes_file(project_id):
    """
    uploads the test data and saves it as test_data.csv in the working directory
    :param project_id: the ID of the current project
    :return: returns 204 if the file was saved successfully
    """
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    print("saving facettes file for " + project_id)
    file = request.files['facettes']
    path_to_save = location + '/out/' + project_id + '/'
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    try:
        file.save(path_to_save + 'facettes.csv')
        return Response('facettes saved', status=204)
    except IOError:
        return Response('could not write file', status=500)


@cross_origin('*')
@facettes_blueprint.route('/journal_list/<project_id>')
def retrieve_journal_facettes_list(project_id):
    """
    loads the list of top journals from the facettes file. the number of top journals is given as path parameter
    'sample-size', default is 20.
    :param project_id: the ID of the current project
    :return: a list of journals with the given sample size
    """

    sample_size = int(request.args.get('sample_size', default='20'))
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    journal_facettes = []
    with open(location + '/out/' + project_id + '/' + 'facettes.csv', 'r', encoding='utf-8-sig') as csvfile:
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

            journal_facettes.append({'journal': row[12], 'count': int(row[13])})
        csvfile.close()
    with open(location + '/out/' + project_id + '/' + 'journal_facettes.txt', 'w', encoding='utf-8') as facettes_file:
        for journal_facette in journal_facettes:
            facettes_file.write(journal_facette['journal'] + '\n')
        facettes_file.close()
    return jsonify(journal_facettes[:sample_size])


@facettes_blueprint.route('/generate_lists/<project_id>', methods=['POST'])
def generate_lists(project_id):
    """
    generates the list of top journals and top keywords from the facettes file.
    :param project_id: the ID of the current project
    :return: returns a 204, if the file was created successfully.
    """
    try:
        facettes_service.generate_lists(project_id)
        return Response('list files generated', status=204)
    except IOError:
        return Response('could not write file', status=500)


@cross_origin('*')
@facettes_blueprint.route('/keyword_list/<project_id>')
def retrieve_keyword_facettes_list(project_id):
    """
    loads the list of top keywords from the facettes file. the number of top keywords is given as path parameter
    'sample-size', default is 20.
    :param project_id: the ID of the current project
    :return: a list of keywords of the given sample size
    """
    sample_size = int(request.args.get('sample_size', default='20'))
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    keyword_facettes = []
    with open(location + '/out/' + project_id + '/' + 'facettes.csv', 'r', encoding='utf-8-sig') as csvfile:
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
    with open(location + '/out/' + project_id + '/' + 'keyword_facettes.txt', 'w', encoding='utf-8') as facettes_file:
        for keyword_facette in keyword_facettes:
            facettes_file.write(keyword_facette['keyword'] + '\n')
        facettes_file.close()
    return jsonify(keyword_facettes[:sample_size])
