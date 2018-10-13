import json
import requests
import os
import scopus
import pickle

from flask import Flask
from flask import request
from elasticsearch import Elasticsearch

from model.AllResponses import AllResponses
from altmetric.Altmetric import Altmetric
from unpaywall.Unpaywall import Unpaywall
from utilities import utils

es = Elasticsearch()

# configure FLASK and get the parameters from the settings file
app = Flask(__name__)

# initialize config file from environment variable
app.config.from_envvar("LIBINTEL_SETTINGS")

# read the parameters form the config file
location = app.config.get("LIBINTEL_DATA_DIR")
altmetric_key = app.config.get("ALTMETRIC_API_KEY")
altmetric_secret = app.config.get("ALTMETRIC_API_SECRET")
scopus_api_key = app.config.get("SCOPUS_API_KEY")
libintel_user_email = app.config.get("LIBINTEL_USER_EMAIL")

# initialize the API connectors for Unpaywall and Altmetric.
altmetric = Altmetric()
altmetric.set_key(altmetric_key)
altmetric.set_secret(altmetric_secret)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/query_execution', methods=['POST'])
def query_execution():
    # load the search queries from the http POST body
    search = request.get_json(silent=True)

    print(search)

    # get the identifier from the set, this will determine the index in elasticsearch
    query_id = search['query_id']

    # prepare location for saving data
    out_dir = location + '/out/' + query_id + '/'
    if not os.path.exists(location):
        os.makedirs(location)

    # convert the JSON search object to the search string for the scopus api
    search_string = utils.convert_search_to_scopus_search_string(search)

    print(search_string)

    # perform the search in Scopus
    search = scopus.ScopusSearch(search_string, refresh=True)

    # retrieve the EIDs
    eids = search.EIDS

    total_number_of_results = eids.__len__()

    print('found ' + str(total_number_of_results) + ' in Scopus')

    # persist EIDs to file to be uploaded to Scival
    save_eids_to_file(eids, out_dir)

    # for each EID , create a AllResponses object and attach the full data set from scopus,
    # the altmetric response and the unpaywall response
    if eids.__len__() > 0:

        responses = []
        for idx, eid in enumerate(eids):
            # print progress
            print('processing entry ' + str(idx) + 'of ' + str(total_number_of_results) + ' entries: ' + str(idx/total_number_of_results * 100) + '%')

            # retrieve data from scopus
            scopus_abstract = scopus.ScopusAbstract(eid, view="FULL")

            # create new AllResponses object to hold the individual information
            response = AllResponses(eid)

            # add scopus abstract to AllResponses object
            response.scopus_abtract_retrieval = scopus_abstract

            # get doi and collect unpaywall data and Altmetric data
            doi = scopus_abstract.doi
            if doi is not "":
                response.unpaywall_response = Unpaywall(libintel_user_email, doi)
                # response.altmetric_response = altmetric.get_data_for_doi(doi)

            # add response to list of responses
            responses.append(response)

            # send response to elastic search index
            send_to_index(response, query_id)

            # save_to_file(response, out_dir)

    return 'ok'


# to be changed, persist via posting
# TO DO: replace posting by persisting in database. Agree on data structure
def persist_list(scopus_responses):
    payload = json.dumps([ob.__dict__ for ob in scopus_responses])
    url = 'http://localhost:11200/ebsData/saveList'
    headers = {'content-type': 'application/json'}
    post = requests.post(url, data=payload, headers=headers)
    print(post.status_code)


def save_eids_to_file(eids, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + 'eids_list.txt', 'w') as list_file:
        for eid in eids:
            list_file.write(eid + '\n')
    print('saved results to disk')


def send_to_index(all_responses: AllResponses, query_id):
    all_responses_json = json.dumps(all_responses, cls=HiddenEncoder)
    res = es.index(query_id, 'all_data', all_responses_json, all_responses.id)
    print('saved to index ' + query_id)
    return res


# persist the resulting json document on disk
def save_to_file(documents, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + 'data_out.json', 'w') as json_file:
        json.dump(documents, json_file)
    print('saved results to disk')

class HiddenEncoder(json.JSONEncoder):
    def default(self, o):
        return {k.lstrip('_'): v for k, v in o.__getstate__().items()}
