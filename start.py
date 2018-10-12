import csv
import json
import requests
import os
import hashlib
import scopus

from flask import Flask
from flask import request
from elasticsearch import Elasticsearch

from model.AllResponses import AllResponses
from model.Unpaywall import Unpaywall
from utilities import utils

es = Elasticsearch()

# configure FLASK and get the parameters from the settings file
app = Flask(__name__)
# app.config.from_object('yourapplication.default_settings')
app.config.from_envvar("LIBINTEL_SETTINGS")

location = app.config.get("LIBINTEL_DATA_DIR")
elsevier_url = app.config.get("ELSEVIER_URL")
altmetric_url = app.config.get("ALTMETRIC_URL")
altmetric_key = app.config.get("ALTMETRIC_API_KEY")
altmetric_secret = app.config.get("ALTMETRIC_API_SECRET")
scopus_api_key = app.config.get("SCOPUS_API_KEY")
unpaywall_api_url = app.config.get("UNPAYWALLL_API_URL")
libintel_user_email = app.config.get("LIBINTEL_USER_EMAIL")

unpaywall = Unpaywall(libintel_user_email)


@app.route('/query_execution', methods=['POST'])
def query_execution():
    # prepare location for saving data
    if not os.path.exists(location):
        os.makedirs(location)

    # load the search queries from the http POST body
    search = request.get_json(silent=True)

    print(search)

    # get the identifier from the set, this will determine the index in elasticsearch
    query_id = search['query_id']

    # convert the JSON search object to the search string for the scopus api
    search_string = utils.convert_search_to_scopus_search_string(search)

    print(search_string)

    # perform the search in Scopus
    search = scopus.ScopusSearch(search_string, refresh=True)

    # retrieve the EIDs
    eids = search.EIDS

    total_number_of_results = eids.__len__()

    print('found ' + str(total_number_of_results) + ' in Scopus')

    # save_eids_to_file(eids)

    # for each EID , create a AllResponses object and attach the full data set from scopus,
    # the altmetric response and the unpaywall response
    if eids.__len__() > 0:

        responses = []
        for idx, eid in enumerate(eids):


            print('processing entry ' + str(idx) + 'of ' + str(total_number_of_results) + ' entries: ' + str(idx/total_number_of_results * 100) + '%')

            # retrieve data from scopus
            scopus_abstract = scopus.ScopusAbstract(eid, view="FULL")

            # create new AllResponses object to hold the individual information
            response = AllResponses(eid)

            # add scopus abstract to AllResponses object
            response.scopusAbtractRetrieval = scopus_abstract

            # get doi and collect unpaywall data and Altmetric data
            doi = scopus_abstract.doi
            if doi is not "":
                response.UnpaywallResponse = get_unpaywall_data(doi)
                response.AltmetricResponse = get_altmetric_data(doi)

            # add response to list of responses
            responses.append(response)

            # send response to elastic search index
            send_to_index(response, query_id)


    return 'ok'
    # define the number of results for further requests
    results_per_page = 100

    # define the url to be queried, first of all get only the number of results, hence only 1 result per page
    url = elsevier_url + '/content/search/scopus?count=1&query=' + search_string.replace(" ", "+") + '&apiKey=' + scopus_api_key
    print("querying URL: " + url)

    # perform the query
    r = requests.get(url)
    if r.status_code == 200:
        # convert response to JSON object
        scopus_first_response = r.json()

        # read the total number of results
        number_of_results = int(scopus_first_response['search-results']['opensearch:totalResults'])
        print('total number of publications for this query: ' + str(number_of_results))

        publication_set = []

        # if results have been found, query all the results
        if number_of_results != 0:

            # calculate the number of requests necessary
            number_of_calls = number_of_results // results_per_page + 1

            # perform the individual calls
            for i in range(number_of_calls):
                start = i * results_per_page
                url = elsevier_url + '/content/search/scopus?start=' + str(start) + '&count=' + str(results_per_page) + '&query=' + search_string + '&apiKey=' + scopus_api_key
                r = requests.get(url)

                # if results are obtained create a ScopusResponse object with all the necessary identifiers accessible.
                if r.status_code == 200:
                    for document in r.json()['search-results']['entry']:
                        print(document)
                        # now we query scopus for citation information, Altmetric for societal impact
                        # and Unpaywall for the Open Access information.
                        # each response is added to the intial Scopus response object
                        # doing this within the loop reduces the "pressure" on the APIs
                        extendData(document)

                        # then we save the extended document to an elastic search index.
                        # from this index, we can construct the table used for further analysis.
                        send_to_index(document, query_id)

                        # add the complete scopus response object to the list
                        publication_set.append(document)
            save_to_file(publication_set)
    return "OK"


def extendData(publication):
    # first get the complete set of data from Scopus
    get_extended_data_from_scopus(publication)

    # then the extended citation data from Scopus
    # get_citation_data_from_scopus(publication)

    # get impact data from altmetrics
    get_altmetric_data(publication)

    # then retrieve the Open Access data from Unpaywall
    get_unpaywall_data(publication)


# to be changed, persist via posting
# TO DO: replace posting by persisting in database. Agree on data structure
def persist_list(scopus_responses):
    payload = json.dumps([ob.__dict__ for ob in scopus_responses])
    url = 'http://localhost:11200/ebsData/saveList'
    headers = {'content-type': 'application/json'}
    post = requests.post(url, data=payload, headers=headers)
    print(post.status_code)


def send_to_index(document, query_id):
    res = es.index(query_id, 'full-data', document)
    print('saved to index ' + query_id)
    return res['result']


def send_to_index(all_responses: AllResponses, query_id):
    scopus_response = all_responses.scopusAbtractRetrieval
    res = es.index(query_id, 'scopus_abstract', scopus_response.toJSON(), all_responses.id)
    print('saved to index ' + query_id)
    return res['result']


# persist the resulting json document on disk
def save_to_file(documents):
    out_dir = location + '/out/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + 'data_out.json', 'w') as json_file:
        json.dump(documents, json_file)
    print('saved results to disk')


def get_extended_data_from_scopus(document):
    if document['prism:doi'] is not None:
        url = elsevier_url + '/content/abstract/doi/' + document['prism:doi'] + '?apiKey=' + scopus_api_key + '&httpAccept=application%2Fjson'
        r = requests.get(url)
        print("queryied URL: " + url + " with status code " + str(r.status_code))
        if r.status_code == 200:
            response = r.json()
            try:
                del response['abstracts-retrieval-response']['item']
            except KeyError:
                print('no additional classification')
            document['extended_data'] = response


def get_citation_data_from_scopus(document):
    if document['prism:doi'] is not None:
        url = elsevier_url + '/content/abstract/citations?doi=' + document['prism:doi'] + '&apiKey=' + scopus_api_key
        r = requests.get(url)
        print("queryied URL: " + url + " with status code " + str(r.status_code))
        if r.status_code == 200:
            document['citation_response'] = r.json()


def get_unpaywall_data(doi):
        url = unpaywall_api_url + '/' + doi + "?email=" + libintel_user_email
        r = requests.get(url)
        print("queryied URL: " + url + " with status code " + str(r.status_code))
        if r.status_code == 200:
            return r.json()


def get_altmetric_data(doi):

    url = altmetric_url + '/doi/' + doi + '?key=' + altmetric_key
    r = requests.get(url)
    print("queryied URL: " + url + " with status code " + str(r.status_code))
    if r.status_code == 200:
        return r.json()
    # filters = ''
    # searchterm = []
    # for term in searchterm:
    #   filters += '|' + term
    # digest = hashlib.sha1()
    # first_digest = digest.sha1(filters)
    # second_digest = first_digest.update(altmetric_secret)


