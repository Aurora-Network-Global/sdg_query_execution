import json
import os
from json import JSONDecodeError

import scopus
import numpy as np
import csv
import random
# import pytextrank

from flask import Flask, send_file, jsonify, request, Response
from flask_cors import CORS
from elasticsearch import Elasticsearch

from model.AbstractText import AbstractText
from model.AllResponses import AllResponses
from altmetric.Altmetric import Altmetric
from model.Query import Query
from model.RelevanceMeasures import RelevanceMeasure
from model.ScivalUpdate import ScivalUpdate
from model.Status import Status
from model.UpdateContainer import UpdateContainer
from scival.Scival import Scival
from unpaywall.Unpaywall import Unpaywall
from utilities import utils

es = Elasticsearch()

# configure FLASK and get the parameters from the settings file
app = Flask(__name__)
CORS(app)

# initialize config file from environment variable
app.config.from_envvar("LIBINTEL_SETTINGS")

# read the parameters form the config file
location = app.config.get("LIBINTEL_DATA_DIR")
altmetric_key = app.config.get("ALTMETRIC_API_KEY")
altmetric_secret = app.config.get("ALTMETRIC_API_SECRET")
scopus_api_key = app.config.get("SCOPUS_API_KEY")
libintel_user_email = app.config.get("LIBINTEL_USER_EMAIL")


# ----------------------------------- query repository -----------------------------------------------------------------

@app.route("/query/single/<query_id>", methods=['GET'])
def get_query(query_id):
    path_to_file = location + '/out/' + query_id + '/query.json'
    try:
        with open(path_to_file) as json_file:
            query = json.load(json_file)
            json_file.close()
            return jsonify(query)
    except FileNotFoundError:
        query = Query()
        return jsonify(query.__dict__)


# retrieves the Scopus search string and to display it in the browser
@app.route("/query/scopusSearchString/<query_id>", methods=['GET'])
def get_scopus_search_string(query_id):
    path_to_file = location + '/out/' + query_id + '/scopus_search_string.txt'
    try:
        with open(path_to_file) as json_file:
            search_string = json_file.read()
            json_file.close()
            return Response(search_string, status=200)
    except FileNotFoundError:
        return Response("File not found", status=404)


# saves the query as json document in the working directory as query.json file
@app.route("/query/single/<query_id>", methods=['POST'])
def save_query(query_id):
    if request.method == 'POST':
        project = open_project(query_id)
        query = request.get_json(silent=True)
        json_string = json.dumps(query)
        out_dir = location + '/out/' + query_id + '/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(out_dir + 'query.json', 'w') as json_file:
            json_file.write(json_string)
            json_file.close()

        # convert the JSON search object to the search string for the scopus api
        search_string = utils.convert_search_to_scopus_search_string(query)
        with open(out_dir + 'scopus_search_string.txt', 'w') as scopus_search_string_file:
            scopus_search_string_file.write(search_string)
            scopus_search_string_file.close()
        project['isQueryDefined'] = True
        save_project(project)
        return jsonify(query)
    else:
        return Response("Use POST", status=405)
    

# ----------------------------------- project repository ---------------------------------------------------------------

@app.route("/project/all", methods=['GET'])
def list_projects():
    projects = []
    list_filenames = os.listdir(location + '/out/')
    for filename in list_filenames:
        if filename.endswith('.json'):
            path_to_file = location + '/out/' + filename
            try:
                with open(path_to_file) as json_file:
                    project = json.load(json_file)
                    json_file.close()
                    projects.append(project)
            except FileNotFoundError:
                continue
    return jsonify(projects)


# loads a project by the project ID
@app.route("/project/single/<project_id>", methods=['GET'])
def get_project(project_id):
    try:
        return jsonify(open_project(project_id))
    except FileNotFoundError:
        return Response("File not found", status=404)


# saves a project
@app.route("/project", methods=['post'])
def save_posted_project():
    project = request.get_json(silent=True)
    save_project(project)
    project_dir = location + '/out/' + project['project_id']
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    return jsonify(project)


def open_project(project_id):
    path_to_file = location + '/out/' + project_id + '.json'
    with open(path_to_file) as json_file:
        project = json.load(json_file)
        json_file.close()
        return project


def save_project(project):
    json_string = json.dumps(project)
    out_dir = location + '/out/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + project['project_id'] + '.json', 'w') as json_file:
        json_file.write(json_string)


# ----------------------------------- EIDs repository ------------------------------------------------------------------
# download the file with the EIDs from the search, stored in the working directory as eids_list.txt
@app.route("/eids/all/<query_id>", methods=['GET'])
def get_eids(query_id):
    # path to the file
    path_to_file = location + '/out/' + query_id + '/' + 'eids_list.txt'
    try:
        return send_file(path_to_file, attachment_filename='eids_list.txt')
    except IOError:
        return Response('no list of missed eids', status=404)


def open_eids(query_id, prefix):
    # path to the file
    out_dir = location + '/out/' + query_id + '/'
    with open(out_dir + prefix + 'eids_list.txt') as f:
        eids = f.readlines()
        f.close()
        # remove whitespace characters like `\n` at the end of each line
    return [x.strip() for x in eids]


# download the file with the missed EIDs from the search, stored in the working directory as missed_eids_list.txt
@app.route("/eids/missed/<query_id>", methods=['GET'])
def download_missed_eids(query_id):
    # path to the file
    path_to_file = location + '/out/' + query_id + '/' + 'missed_eids_list.txt'
    try:
        return send_file(path_to_file, attachment_filename='missed_eids_list.txt')
    except IOError:
        return Response('no list of missed eids', status=404)


# download the file with the missed EIDs from the search, stored in the working directory as missed_eids_list.txt
@app.route("/eids/calculateSample/<query_id>", methods=['GET'])
def calculate_sample(query_id):
    sample_size = int(request.args.get('sample_size'))
    print(sample_size)
    if sample_size is None:
        sample_size = 10
    # path to the file
    out_dir = location + '/out/' + query_id + '/'
    with open(out_dir + 'eids_list.txt') as file:
        eids = file.readlines()
        file.close()
        eids = [x.strip() for x in eids]
    number = eids.__len__()
    random_sample_eids = []
    if number > sample_size:
        test_indices = random.sample(range(1, eids.__len__()), sample_size)
        for index, value in enumerate(eids):
            if index in test_indices:
                random_sample_eids.append(value)
        save_eids_to_file(random_sample_eids, query_id, 'sample_')
    else:
        save_eids_to_file(eids, query_id, 'sample_')
    try:
        return send_file(out_dir + 'sample_eids_list.txt', attachment_filename='missed_eids_list.txt')
    except FileNotFoundError:
        return Response('no list of sample eids', status=404)


# check the provided test EIDs vs the obtained result set
@app.route("/eids/checkTestEids/<query_id>", methods=['GET'])
def check_test_eids(query_id):
    out_dir = location + '/out/' + query_id + '/'
    # open test data and read eids
    with open(out_dir + 'test_data.txt') as f:
        test_eids = f.readlines()
        f.close()
        # remove whitespace characters like `\n` at the end of each line
        test_eids = [x.strip() for x in test_eids]
    # open collected data and read eids
    with open(out_dir + 'eids_list.txt') as f:
        eids = f.readlines()
        f.close()
        # remove whitespace characters like `\n` at the end of each line
        eids = [x.strip() for x in eids]
    relevance_measure = RelevanceMeasure()
    relevance_measure.total_number_of_query_results = eids.__len__()
    relevance_measure.number_of_test_entries = test_eids.__len__()
    for test_eid in test_eids:
        if test_eid in eids:
            relevance_measure.true_positives = relevance_measure.true_positives + 1
    relevance_measure.false_negatives = relevance_measure.number_of_test_entries - relevance_measure.true_positives
    if relevance_measure.total_number_of_query_results > 0:
        relevance_measure.precision = relevance_measure.true_positives / relevance_measure.number_of_test_entries
    else:
        relevance_measure.precision = 0
    save_relevance_measures_to_file(relevance_measure, out_dir)
    return jsonify(relevance_measure.__dict__)


# download the file with the missed EIDs from the search, stored in the working directory as missed_eids_list.txt
@app.route("/eids/sample/<query_id>", methods=['GET'])
def download_sample_eids(query_id):
    # path to the file
    path_to_file = location + '/out/' + query_id + '/' + 'test_sample_eids_list.txt'
    try:
        return send_file(path_to_file, attachment_filename='test_sample_eids_list.txt')
    except IOError:
        return Response('no list of missed eids', status=404)


def save_eids_to_file(eids, project_id, prefix=''):
    out_dir = location + '/out/' + project_id + '/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + prefix + 'eids_list.txt', 'w') as list_file:
        for eid in eids:
            list_file.write(eid + '\n')
        list_file.close()
    print('saved results to disk')


# returns true if the eids_list.txt file is present for the given project
@app.route("/eids/check/<query_id>")
def check_eids(query_id):
    path_to_file = location + '/out/' + query_id + '/eids_list.txt'
    return jsonify(os.path.exists(path_to_file))


# uploads the test data and saves it as test_data.csv in the working directory
@app.route('/eids/test/<query_id>', methods=['POST'])
def upload_test_file(query_id):
    print("saving test file for " + query_id)
    if request.method == 'POST':
        project = open_project(query_id)
        file = request.files['test-file']
        path_to_save = location + '/out/' + query_id + '/'
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        file.save(path_to_save + 'test_data.txt')
        project['isTestdata'] = True
        save_project(project)
    return Response("OK", status=204)


# ----------------------------------- Status repository ----------------------------------------------------------------
# reads the status file (status.json) and returns it.
@app.route("/status/single/<query_id>")
def get_status(query_id):
    path_to_file = location + '/out/' + query_id + '/status.json'
    try:
        with open(path_to_file) as json_file:
            status = json.load(json_file)
            json_file.close()
            return jsonify(status)
    except FileNotFoundError:
        status = Status("ERROR")
        return jsonify(status.__dict__)
    except JSONDecodeError:
        status = Status("STARTING")
        return jsonify(status.__dict__)


def save_status(status, out_dir):
    print('saving status')
    with open(out_dir + 'status.json', 'w') as json_file:
        print(status.__dict__)
        json.dump(status.__dict__, json_file)
        json_file.close()


# ----------------------------------- Relevance measures repository ----------------------------------------------------
# reads the relavance measures file (relevance_measures.json) and returns it.
@app.route("/relevanceMeasures/single/<query_id>")
def get_relevance_measures(query_id):
    path_to_file = location + '/out/' + query_id + '/relevance_measures.json'
    try:
        with open(path_to_file) as json_file:
            relevance_measures = json.load(json_file)
            json_file.close()
            return jsonify(relevance_measures)
    except FileNotFoundError:
        return Response("File not found", status=404)


def save_relevance_measures_to_file(relevance_measures, out_dir):
    with open(out_dir + 'relevance_measures.json', 'w') as json_file:
        json_file.write(json.dumps(relevance_measures.__dict__))
        json_file.close()


# ----------------------------------- Scival data repository -----------------------------------------------------------
# returns true if the scival_data.csv file is present for the iven project
@app.route("/scival/check/<query_id>")
def check_scival(query_id):
    path_to_file = location + '/out/' + query_id + '/scival_data.csv'
    return jsonify(os.path.exists(path_to_file))


# uploads the scival data and saves it as scival_data.csv in the working directory
@app.route('/scival/single/<query_id>', methods=['POST'])
def upload_scival_file(query_id):
    print("saving scival file for " + query_id)
    if request.method == 'POST':
        project = open_project(query_id)
        file = request.files['scival-file']
        path_to_save = location + '/out/' + query_id + '/'
        print(path_to_save)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        file.save(path_to_save + 'scival_data.csv')
        project['isScivalData'] = True
        save_project(project)
        import_scival_data(query_id)
    return Response("OK", status=204)


# reads in the scival data and uses the results to update the elasticsearch index
@app.route('/scival/import/<query_id>', methods=['GET'])
def import_scival_data(query_id):
    with open(location + '/out/' + query_id + '/' + 'scival_data.csv', 'r') as csvfile:
        scivals = []
        linereader = csv.reader(csvfile, delimiter=',')
        for row in linereader:
            if row.__len__() != 32:
                continue
            if row[0] == 'Title':
                continue
            scival = Scival(row)
            append_to_index(ScivalUpdate(scival), scival.eid, query_id)
            scivals.append(scival)
        csvfile.close()
    return "imported " + str(scivals.__len__()) + " Scival data"


# ----------------------------------- elasticsearch connections --------------------------------------------------------

def send_to_index(all_responses: AllResponses, query_id):
    all_responses_json = json.dumps(all_responses, cls=HiddenEncoder)
    res = es.index(query_id, 'all_data', all_responses_json, all_responses.id, request_timeout=600)
    print('saved to index ' + query_id)
    return res


def append_to_index(document, eid, query_id):
    update_container = UpdateContainer(document)
    update_json = json.dumps(update_container, cls=HiddenEncoder)
    res = es.update(index=query_id, doc_type="all_data", id=eid, body=update_json)
    print('saved to index ' + query_id)
    return res


# ----------------------------------- keywords endpoint ----------------------------------------------------------------
# retrieve the list of keywords for the search
@app.route("/keywords/<query_id>")
def get_keywords(query_id):
    try:
        result = es.search(index=query_id, doc_type='all_data',
                           filter_path=["hits.hits._source.scopus_abtract_retrieval.authkeywords", "hits.hits._id"])
        keyword_list = []
        for hit in result["hits"]["hits"]:
            keyword_list.extend(hit["_source"]["scopus_abtract_retrieval"]["authkeywords"])
        dictionary = utils.wordlist_to_freq_dict(keyword_list)
        sorted_dict = utils.sort_freq_dict(dictionary)
        return json.dumps([ob.__dict__ for ob in sorted_dict])
    except IOError:
        return Response('no keywords ', status=404)


# ----------------------------------- execution endpoint ---------------------------------------------------------------
# executes the defined and saved query in scopus
@app.route('/query/execution/<query_id>', methods=['POST'])
def query_execution(query_id):
    # prepare location for saving data
    out_dir = location + '/out/' + query_id + '/'
    if not os.path.exists(location):
        return Response("query not yet defined", status=404)

    # reads the saved Scopus search string from disk
    with open(out_dir + 'scopus_search_string.txt') as json_file:
        search_string = json_file.read()
        json_file.close()

    # retrieve the project from disk
    project = open_project(query_id)

    # prepares the status file
    status = Status("EIDS_COLLECTING")
    save_status(status, out_dir)

    project['isEidsCollected'] = False
    project['isEidsCollecting'] = True
    save_project(project)

    # perform the search in Scopus
    search = scopus.ScopusSearch(search_string, refresh=True, query_id=query_id)

    # retrieve the EIDs
    eids = search.EIDS

    # set the total number of results to the relevance measure save it to disk
    relevance_measure = RelevanceMeasure()
    relevance_measure.total_number_of_query_results = eids.__len__()
    save_relevance_measures_to_file(relevance_measure, out_dir)

    # set the total number of results to the status save it to disk
    status.total = relevance_measure.total_number_of_query_results
    save_status(status, out_dir)

    # print the results to the command line for logging
    print('found ' + str(eids.__len__()) + ' in Scopus')

    # persist EIDs to file
    save_eids_to_file(eids, query_id)

    # set the status and save it to disk
    status = Status("EIDS_COLLECTED")
    save_status(status, out_dir)

    # set the project boolean and save the project
    project['isEidslist'] = True
    project['isEidsCollected'] = True
    project['isEidsCollecting'] = False
    save_project(project)

    return Response({"status": "FINISHED"}, status=204)


@app.route('/collect_data/<query_id>', methods=['POST'])
def data_collection_execution(query_id):
    project = open_project(query_id)
    missed_eids = []
    out_dir = location + '/out/' + project['project_id'] + '/'
    path_to_eids = out_dir + 'eids_list.txt'
    status = Status("DATA_COLLECTING")
    with open(path_to_eids) as file:
        eids = file.readlines()
        file.close()
        eids = [x.strip() for x in eids]
    status.total = eids.__len__()

    if status.total > 0:
        es.indices.delete(project['project_id'], ignore=[400, 404])
        for idx, eid in enumerate(eids):
            # update the progress status and save the status to disk
            status.progress = idx + 1
            save_status(status, out_dir)

            # print progress
            print('processing entry ' + str(idx) + 'of ' + str(status.total) + ' entries: ' +
                  str(idx / status.total * 100) + '%')

            # retrieve data from scopus
            try:
                scopus_abstract = scopus.ScopusAbstract(eid, view="FULL")
            except IOError:
                missed_eids.append(eid)
                continue

            # create new AllResponses object to hold the individual information
            response = AllResponses(eid, project['name'], project['project_id'])

            # add scopus abstract to AllResponses object
            response.scopus_abtract_retrieval = scopus_abstract

            # get doi and collect unpaywall data and Altmetric data
            doi = scopus_abstract.doi
            if doi is not "":
                if doi is not None:
                    response.unpaywall_response = Unpaywall(libintel_user_email, doi)
                    response.altmetric_response = Altmetric(altmetric_key, doi)
                    response.scival_data = Scival([])

            # send response to elastic search index
            send_to_index(response, project['project_id'])
    save_eids_to_file(missed_eids, project['project_id'], 'missed_')

    status.status = "DATA_COLLECTED"
    save_status(status, out_dir)

    project['isQueryRun'] = True
    save_project(project)
    return Response({"status": "FINISHED"}, status=204)


@app.route('/prepare_abstracts/<query_id>', methods=['POST'])
def count_keywords(query_id):
    project = open_project(query_id)
    out_dir = location + '/out/' + project['project_id'] + '/'
    result = es.search(index=project['project_id'], doc_type='all_data',
                       filter_path=["hits.hits._source.scopus_abtract_retrieval.abstract", "hits.hits._id"],
                       request_timeout=600)
    keyword_list = []
    for hit in result["hits"]["hits"]:
        keyword_list.append(AbstractText(hit['_id'], hit["_source"]["scopus_abtract_retrieval"]["abstract"]))
    with open(out_dir + 'abstracts.json', 'w') as json_file:
        json_file.write(json.dumps([ob.__dict__ for ob in keyword_list]))
        json_file.close()
    return Response({"status": "FINISHED"}, status=204)


# @app.route("/calculateTextrank/<query_id>")
# def calculate_text_rank(query_id):
#     path_to_file = location + '/out/' + query_id + '/abstracts.json'
#     for graf in pytextrank.parse_doc(pytextrank.json_iter(path_to_file)):
#         print(pytextrank.pretty_print(graf))
#     return "ok"

@app.route('/analysis/overlap', methods=['GET'])
def calculate_overlap():
    print('calculating overview')
    list_ids = request.args.getlist('primary')
    second_list = request.args.getlist('secondary')
    if second_list.__len__() == 0:
        array = calculate_symmetric_overlap(list_ids)
        length_func = np.vectorize(get_length)
        print(length_func(array))
        return Response({"status": "FINISHED"}, status=200)
    else:
        calculate_asymmetric_overlap(list_ids, second_list)
        return Response({"status": "FINISHED"}, status=200)


def get_length(x):
    if x is not None:
        return len(x)
    else:
        return 0


def calculate_symmetric_overlap(primary):
    primary_length = len(primary)
    overlap_map = np.empty((primary_length, primary_length), dtype=object)
    data = {}
    for key in primary:
        data[key] = open_eids(key, '')
    for i in range(0, primary_length):
        for entry in data[primary[i]]:
            found = False
            for j in range(i+1, primary_length):
                if entry in data[primary[j]]:
                    if overlap_map[i, j] is None:
                        overlap_map[i, j] = [entry]
                        overlap_map[j, i] = [entry]
                    else:
                        overlap_map[i, j].append(entry)
                        overlap_map[j, i].append(entry)
                    found = True
            if not found:
                if overlap_map[i, i] is None:
                    overlap_map[i, i] = [entry]
                else:
                    overlap_map[i, i].append(entry)
    return overlap_map


def calculate_asymmetric_overlap(primary, secondary):
    primary_length = primary.__len__()
    secondary_length = secondary.__len__()
    overlap_map = np.empty((primary_length, secondary_length), dtype=object)
    data = {}
    for key in primary:
        data[key] = open_eids(key, '')
    for key in secondary:
        data[key] = open_eids(key, '')
    for i in range(0, primary_length):
        for entry in data[primary[i]]:
            found = False
            for j in range(0, secondary):
                if j == i:
                    continue
                if entry in data[secondary[j]]:
                    if overlap_map[i, j] is None:
                        overlap_map[i, j] = [entry]
                    else:
                        overlap_map[i, j].append(entry)
                    found = True
            if not found:
                if overlap_map[i, i] is None:
                    overlap_map[i, i] = [entry]
                else:
                    overlap_map[i, i].append(entry)
    return overlap_map


class HiddenEncoder(json.JSONEncoder):
    def default(self, o):
        return {k.lstrip('_'): v for k, v in o.__getstate__().items()}
