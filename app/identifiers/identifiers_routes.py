#################
#    imports    #
#################
import json
import os
import random

from flask import send_file, Response, request, jsonify
from flask_cors import cross_origin
from pybliometrics import scopus

from model.RelevanceMeasures import RelevanceMeasure
import utilities.utils as utils
from service import eids_service, project_service, relevance_measure_service, query_service, scopus_service, \
    identifier_service
from service.elasticsearch_service import PropertyEncoder
from . import identifiers_blueprint
from flask import current_app as app


################
#    routes    #
################


# download the file with the EIDs from the search, stored in the working directory as eids_list.txt
@identifiers_blueprint.route("/<project_id>/query/<query_id>/identifier", methods=['GET'])
def download_standard_identifier_file(project_id, query_id):
    """
    download the complete list of EIDs
    :param query_id: the ID of the current query
    :param project_id: the ID of the current project
    :return: a txt file containing the EIDs
    """
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    # path to the file
    path_to_file = utils.get_path(location=location, project_id=project_id, query_id=query_id, filename='identifier_list.txt')
    print('sending file ' + path_to_file)
    try:
        return send_file(path_to_file, attachment_filename='eids_list.txt')
    except FileNotFoundError:
        return Response('no list of eids', status=404)


# download the file with the EIDs from the search, stored in the working directory as eids_list.txt
@identifiers_blueprint.route("/<project_id>/query/<query_id>/identifier/<prefix>", methods=['GET'])
def download_identifier_file(project_id, query_id, prefix):
    """
    download the complete list of EIDs
    :param prefix: the prefix of the list to be retrieved
    :param query_id: the ID of the current query
    :param project_id: the ID of the current project
    :return: a txt file containing the EIDs
    """
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    # path to the file
    path_to_file = utils.get_path(location=location, project_id=project_id, query_id=query_id, filename='identifier_list.txt',
                                  prefix=prefix)
    print('sending file ' + path_to_file)
    try:
        return send_file(path_to_file, attachment_filename='eids_list.txt')
    except FileNotFoundError:
        return Response('no list of eids', status=404)


@identifiers_blueprint.route("<project_id>/query/<query_id>/lastChange", methods=['GET'])
def get_last_change(project_id, query_id):
    return str(identifier_service.get_last_change(project_id, query_id))


@identifiers_blueprint.route("<project_id>/query/<query_id>/lastChange/<prefix>", methods=['GET'])
def get_data_of_test_eids(project_id, query_id, prefix):
    return str(identifier_service.get_last_change(project_id, query_id, 'test_'))


@cross_origin('*')
@identifiers_blueprint.route("/<project_id>/query/<query_id>/calculateSampleIdentifiers", methods=['GET'])
def retrieve_identifier_sample(project_id, query_id):
    session_id = request.args.get('session')
    sample_size = int(request.args.get('sample_size'))
    if sample_size is None:
        sample_size = 100
    if session_id is None:
        return Response(generate_sample_identifiers_list(project_id, query_id, sample_size, ''), status=200)
    try:
        random_sample_eids = identifier_service.load_id_list(project_id, query_id, session_id + '_' + str(sample_size))
    except:
        random_sample_eids = generate_sample_identifiers_list(project_id, query_id, sample_size, session_id)
    return Response(random_sample_eids, status=200)


@cross_origin('*')
@identifiers_blueprint.route("/<project_id>/query/<query_id>/calculateSamplePublications", methods=['GET'])
def retrieve_publications_sample(project_id, query_id):
    session_id = request.args.get('session')
    sample_size = int(request.args.get('sample_size'))
    if sample_size is None:
        sample_size = 100
    if session_id is None:
        session_id = 'default_session_'
    try:
        random_sample_eids = identifier_service.load_id_list(project_id, query_id, session_id)
    except:
        random_sample_eids = generate_sample_identifiers_list(project_id, query_id, sample_size, session_id)
    search_string = utils.generate_scopus_search_from_eid_list(random_sample_eids)
    search = scopus.ScopusSearch(search_string, refresh=True, project_id=project_id)
    sample_publications_json = json.dumps(search.results, cls=PropertyEncoder)
    return Response(sample_publications_json, status=200, mimetype='application/json')


def generate_sample_identifiers_list(project_id, query_id, sample_size, session_id):
    # path to the file
    eids = identifier_service.load_id_list(project_id, query_id)

    random_sample_eids = []
    if len(eids) > sample_size:
        test_indices = random.sample(range(1, len(eids)), sample_size)
        for index, value in enumerate(eids):
            if index in test_indices:
                random_sample_eids.append(value)
    else:
        random_sample_eids = eids
    if session_id != '':
        identifier_service.save_id_list(project_id, query_id, random_sample_eids, session_id + '_' + str(sample_size))
    else:
        identifier_service.save_id_list(project_id, query_id, random_sample_eids, 'sample')
    return random_sample_eids


# retrieves the Scopus search string and to display it in the browser
@identifiers_blueprint.route("<project_id>/query/>query_id>/scopusSearchString/<prefix>", methods=['GET'])
def get_eids_scopus_search_string(project_id, query_id, prefix):
    try:
        eids = identifier_service.load_id_list(project_id, query_id, prefix)
    except FileNotFoundError:
        sample_size = int(request.args.get('sample_size'))
        eids = generate_sample_identifiers_list(project_id, query_id, sample_size, prefix)
    search_string = 'EID('
    for index, eid in enumerate(eids):
        if index > 0:
            search_string = search_string + ' OR '
        search_string = search_string + eid
    search_string = search_string + ')'
    return Response(search_string, status=200)


# retrieves the Scopus search string and to display it in the browser
@identifiers_blueprint.route("/length/<project_id>", methods=['GET'])
def get_eids_list_length(project_id):
    prefix = request.args.get('prefix')
    try:
        eids = eids_service.load_eid_list(project_id, prefix)
        return Response(str(eids.__len__()), status=200)
    except FileNotFoundError:
        return Response("File not found", status=404)


# retrieves the Scopus search string and to display it in the browser
@identifiers_blueprint.route("/<project_id>/query/<query_id>/identifiers_length", methods=['GET'])
def get_ids_list_length(project_id, query_id):
    prefix = request.args.get('prefix')
    try:
        eids = identifier_service.load_id_list(project_id, query_id, prefix)
        return Response(str(eids.__len__()), status=200)
    except FileNotFoundError:
        return Response("File not found", status=404)


# check the provided test EIDs vs the obtained result set
@identifiers_blueprint.route("/checkTestEids/<project_id>", methods=['GET'])
def check_test_eids(project_id):
    # load test eids
    test_eids = eids_service.load_eid_list(project_id, 'test_')

    # load collected eids
    eids = eids_service.load_eid_list(project_id)
    relevance_measure = relevance_measure_service.load_relevance_measure(project_id)
    if relevance_measure is None:
        relevance_measure = RelevanceMeasure()
    relevance_measure.number_of_search_results = eids.__len__()
    relevance_measure.number_test_entries = test_eids.__len__()
    for test_eid in test_eids:
        if test_eid in eids:
            relevance_measure.number_test_entries_found = relevance_measure.number_test_entries_found + 1
    if relevance_measure.number_of_search_results > 0:
        relevance_measure.recall = relevance_measure.number_test_entries_found / relevance_measure.number_test_entries
    else:
        relevance_measure.recall = 0
    relevance_measure_service.save_relevance_measures(project_id, relevance_measure)
    return jsonify(relevance_measure.__dict__)


# download the file with the missed EIDs from the search, stored in the working directory as missed_eids_list.txt
@identifiers_blueprint.route("/sample/<project_id>", methods=['GET'])
def download_sample_eids(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    # path to the file
    path_to_file = location + '/out/' + project_id + '/' + 'test_sample_eids_list.txt'
    try:
        return send_file(path_to_file, attachment_filename='test_sample_eids_list.txt')
    except FileNotFoundError:
        return Response('no list of missed eids', status=404)


# returns true if the eids_list.txt file is present for the given project
@identifiers_blueprint.route("/check/<project_id>")
def check_eids(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/eids_list.txt'
    return jsonify(os.path.exists(path_to_file))


# uploads the test data and saves it as test_data.csv in the working directory
@identifiers_blueprint.route('/test/<project_id>', methods=['POST'])
def upload_test_file(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    print("saving test file for " + project_id)
    project = project_service.load_project(project_id)
    file = request.files['test-file']
    path_to_save = location + '/out/' + project_id + '/'
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    file.save(path_to_save + 'test_eids_list.txt')
    project['isTestdata'] = True
    project_service.save_project(project)
    return Response('list saved', status=204)


# uploads the test data and saves it as test_data.csv in the working directory
@identifiers_blueprint.route('/sample-judgement/<project_id>', methods=['POST'])
def upload_sample_judgement_file(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    print("saving sample test file for " + project_id)
    project = project_service.load_project(project_id)
    file = request.files['sample-judgement-file']
    path_to_save = location + '/out/' + project_id + '/'
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    file.save(path_to_save + 'sample_judgement_eids_list.csv')
    project.isSampledata = True
    project_service.save_project(project)
    return Response('list saved', status=204)

# check the provided test EIDs vs the obtained result set
@identifiers_blueprint.route("/check_sample/<project_id>", methods=['GET'])
def check_sample_eids(project_id):
    # load collected eids
    eids = eids_service.load_eid_list(project_id)
    relevance_measure = relevance_measure_service.load_relevance_measure(project_id)
    if relevance_measure is None:
        relevance_measure = RelevanceMeasure()
    relevance_measure.number_of_search_results = eids.__len__()
    judgement_list = eids_service.load_judgement_file(project_id)
    relevance_measure['number_sample_entries'] = judgement_list.__len__()
    for judgement in judgement_list:
        if judgement['isRelevant']:
            relevance_measure['number_positive_sample_entries'] = \
                relevance_measure['number_positive_sample_entries'] + 1
    relevance_measure_service.save_relevance_measures(project_id, relevance_measure)
    return jsonify(relevance_measure.__dict__)


@identifiers_blueprint.route('<project_id>/query/<query_id>/executeQuery', methods=['POST'])
def execute_query(project_id, query_id):
    """
    executes the defined and saved query in scopus
    :param project_id: the ID of the current project
    :return: 'finished' with a status of 204 when the query was executed successfully
    """
    print('running project {}'.format(project_id))
    # reads the saved Scopus search string from disk
    scopus_queries = query_service.load_scopus_queries(project_id, query_id)

    # retrieve the project from disk, set the booleans and save the project
    project = project_service.load_project(project_id)
    project.isEidsCollected = False
    project.isEidsCollecting = True
    project_service.save_project(project)

    eids = scopus_service.execute_query(scopus_queries)

    # print the results to the command line for logging
    print('found {} entries in Scopus'.format(len(eids)))

    # persist EIDs to file
    identifier_service.save_id_list(project_id=project_id, query_id=query_id, identifiers=eids)

    # set the project boolean and save the project
    project.isEidslist = True
    project.isEidsCollected = True
    project.isEidsCollecting = False
    project_service.save_project(project)

    return Response({"status": "FINISHED"}, status=204)
