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
from service import eids_service, project_service, relevance_measure_service
from service.elasticsearch_service import PropertyEncoder
from . import eids_blueprint
from flask import current_app as app


################
#    routes    #
################

# download the file with the EIDs from the search, stored in the working directory as eids_list.txt
@eids_blueprint.route("/all/<project_id>", methods=['GET'])
def download_eids(project_id):
    """
    download the complete list of EIDs
    :param project_id: the ID of the current project
    :return: a txt file containing the EIDs
    """
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    # path to the file
    path_to_file = location + '/out/' + project_id + '/' + 'eids_list.txt'
    app.logger.info('project {}: sending file {}'.format(project_id, path_to_file))
    try:
        return send_file(path_to_file, attachment_filename='eids_list.txt')
    except FileNotFoundError:
        app.logger.warn('project {}: could not send file {}'.format(project_id, path_to_file))
        return Response('no list of eids', status=404)


# download the file with the EIDs from the search, stored in the working directory as eids_list.txt
@eids_blueprint.route("/<project_id>/<query_id>/identifier", methods=['GET'])
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
    path_to_file = '{}/out/{}/{}/eids_list.txt'.format(location, project_id, query_id)
    app.logger.info('project {}: sending file {}'.format(project_id, path_to_file))
    try:
        return send_file(path_to_file, attachment_filename='eids_list.txt')
    except FileNotFoundError:
        app.logger.warn('project {}: could not send file {}'.format(project_id, path_to_file))
        return Response('no list of eids', status=404)


# download the file with the EIDs from the search, stored in the working directory as eids_list.txt
@eids_blueprint.route("/<project_id>/<query_id>/identifier/<prefix>", methods=['GET'])
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
    path_to_file = '{}/out/{}/{}/{}_eids_list.txt'.format(location, project_id, query_id, prefix)
    app.logger.info('project {}: sending file {}'.format(project_id, path_to_file))
    try:
        return send_file(path_to_file, attachment_filename='eids_list.txt')
    except FileNotFoundError:
        app.logger.warn('project {}: could not send file {}'.format(project_id, path_to_file))
        return Response('no list of eids', status=404)


# download the file with the missed EIDs from the search, stored in the working directory as missed_eids_list.txt
@eids_blueprint.route("/missed/<project_id>", methods=['GET'])
def download_missed_eids(project_id):
    """
    download the list of missed EIDs
    :param project_id: the ID of the current project
    :return: a txt file containing the EIDs wfor which no full records could be collected
    """
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    # path to the file
    path_to_file = location + '/out/' + project_id + '/' + 'missed_eids_list.txt'
    app.logger.info('project {}: sending file {}'.format(project_id, path_to_file))
    try:
        return send_file(path_to_file, attachment_filename='missed_eids_list.txt')
    except FileNotFoundError:
        app.logger.warn('project {}: could not send file {}'.format(project_id, path_to_file))
        return Response('no list of missed eids', status=404)


@eids_blueprint.route("/lastChange/<project_id>", methods=['GET'])
def get_last_change(project_id):
    return str(eids_service.get_last_change(project_id, ''))


@eids_blueprint.route("/dateOfTest/<project_id>", methods=['GET'])
def get_data_of_test_eids(project_id):
    return str(eids_service.get_last_change(project_id, 'test_'))


@eids_blueprint.route("/dateOfSample/<project_id>", methods=['GET'])
def get_date_of_sample_eids(project_id):
    return str(eids_service.get_last_change(project_id, 'sample_'))


@cross_origin('*')
@eids_blueprint.route("/<project_id>/<query_id>/publicationSample", methods=['GET'])
def retrieve_publications_sample(project_id, query_id):
    session_id = request.args.get('session')
    sample_size = int(request.args.get('sample_size'))
    if sample_size is None:
        sample_size = 100
    if session_id is None:
        session_id = 'default_session_'
    try:
        random_sample_eids = eids_service.load_eid_list(project_id, session_id)
    except:
        random_sample_eids = generate_sample_publication_list(project_id, sample_size, session_id)
    search_string = utils.generate_scopus_search_from_eid_list(random_sample_eids)
    search = scopus.ScopusSearch(search_string, refresh=True, project_id=project_id)
    sample_publications_json = json.dumps(search.results, cls=PropertyEncoder)
    return Response(sample_publications_json, status=200, mimetype='application/json')


@cross_origin('*')
@eids_blueprint.route("/publication_sample/<project_id>", methods=['GET'])
def retrieve_sampled_publications(project_id):
    session_id = request.args.get('session')
    sample_size = int(request.args.get('sample_size'))
    if sample_size is None:
        sample_size = 100
    if session_id is None:
        session_id = 'default_session_'
    try:
        random_sample_eids = eids_service.load_eid_list(project_id, session_id)
    except:
        random_sample_eids = generate_sample_publication_list(project_id, sample_size, session_id)
    search_string = utils.generate_scopus_search_from_eid_list(random_sample_eids)
    search = scopus.ScopusSearch(search_string, refresh=True, project_id=project_id)
    sample_publications_json = json.dumps(search.results, cls=PropertyEncoder)
    app.logger.info('project {}: retrieved {} sample publications for session {}'.format(project_id, sample_size, session_id))
    return Response(sample_publications_json, status=200, mimetype='application/json')


def generate_sample_publication_list(project_id, sample_size, session_id):
    # path to the file
    eids = eids_service.load_eid_list(project_id)

    number = eids.__len__()
    random_sample_eids = []
    if number > sample_size:
        test_indices = random.sample(range(1, eids.__len__()), sample_size)
        for index, value in enumerate(eids):
            if index in test_indices:
                random_sample_eids.append(value)
    else:
        random_sample_eids = eids
    eids_service.save_eid_list(project_id, random_sample_eids, session_id)
    return random_sample_eids


# download the file with the missed EIDs from the search, stored in the working directory as missed_eids_list.txt
@eids_blueprint.route("/calculateSample/<project_id>", methods=['GET'])
def calculate_sample(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    out_dir = location + '/out/' + project_id + '/'
    sample_size = int(request.args.get('sample_size'))
    build_sample_list(project_id, sample_size)
    try:
        app.logger.info('project {}: retrieved sample eid file'.format(project_id))
        return send_file(out_dir + 'sample_eids_list.txt', attachment_filename='sample_eids_list.txt')
    except FileNotFoundError:
        app.logger.error('project {}: could not retrieve sample eid file'.format(project_id))
        return Response('no list of sample eids', status=404, mimetype='text/plain')


def build_sample_list(project_id, sample_size=100):
    if sample_size is None:
        sample_size = 100
    # path to the file
    eids = eids_service.load_eid_list(project_id)

    number = eids.__len__()
    random_sample_eids = []
    if number > sample_size:
        test_indices = random.sample(range(1, eids.__len__()), sample_size)
        for index, value in enumerate(eids):
            if index in test_indices:
                random_sample_eids.append(value)
        eids_service.save_eid_list(project_id=project_id, eids=random_sample_eids, prefix='sample_')
    else:
        eids_service.save_eid_list(project_id=project_id, eids=eids, prefix='sample_')


# retrieves the Scopus search string and to display it in the browser
@eids_blueprint.route("/scopusSearchString/<project_id>", methods=['GET'])
def get_eids_scopus_search_string(project_id):
    prefix = request.args.get('prefix')
    if prefix == 'sample_':
        sample_size = int(request.args.get('sample_size'))
        build_sample_list(project_id, sample_size)
    try:
        eids = eids_service.load_eid_list(project_id, prefix)
    except FileNotFoundError:
        return Response("File not found", status=404)
    search_string = 'EID('
    for index, eid in enumerate(eids):
        if index > 0:
            search_string = search_string + ' OR '
        search_string = search_string + eid
    search_string = search_string + ')'
    return Response(search_string, status=200)


# retrieves the Scopus search string and to display it in the browser
@eids_blueprint.route("/length/<project_id>", methods=['GET'])
def get_eids_list_length(project_id):
    prefix = request.args.get('prefix')
    try:
        eids = eids_service.load_eid_list(project_id, prefix)
        return Response(str(eids.__len__()), status=200)
    except FileNotFoundError:
        return Response("File not found", status=404)


# retrieves the Scopus search string and to display it in the browser
@eids_blueprint.route("/<project_id>/query/<query_id>/identifiers_length", methods=['GET'])
def get_ids_list_length(project_id, query_id):
    prefix = request.args.get('prefix')
    try:
        eids = eids_service.ide(project_id, prefix)
        return Response(str(eids.__len__()), status=200)
    except FileNotFoundError:
        return Response("File not found", status=404)


# check the provided test EIDs vs the obtained result set
@eids_blueprint.route("/checkTestEids/<project_id>", methods=['GET'])
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
@eids_blueprint.route("/sample/<project_id>", methods=['GET'])
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
@eids_blueprint.route("/check/<project_id>")
def check_eids(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/eids_list.txt'
    return jsonify(os.path.exists(path_to_file))


# uploads the test data and saves it as test_data.csv in the working directory
@eids_blueprint.route('/test/<project_id>', methods=['POST'])
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
@eids_blueprint.route('/sample-judgement/<project_id>', methods=['POST'])
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
@eids_blueprint.route("/check_sample/<project_id>", methods=['GET'])
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
