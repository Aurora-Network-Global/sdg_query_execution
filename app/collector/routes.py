from collections import Counter

from flask import Response, request
from pybliometrics import scopus

from multiprocessing import Pool

from altmetric.Altmetric import Altmetric
from model.AllResponses import AllResponses
from model.Status import Status
from scival.Scival import Scival
from service import project_service, status_service, eids_service, \
    elasticsearch_service, counter_service
from unpaywall.Unpaywall import Unpaywall
from . import collector_blueprint


@collector_blueprint.route('/collect_data/<query_id>', methods=['POST'])
def data_collection_execution(query_id):
    # load project and eid list. initialize missed eid list
    project = project_service.load_project(query_id)
    project['isDataCollecting'] = True
    project['isDataCollected'] = False
    eids = eids_service.load_eid_list(query_id)
    missed_eids = []

    status = Status("DATA_COLLECTING")
    status.total = eids.__len__()
    status_service.save_status(query_id, status)

    if status.total > 0:
        elasticsearch_service.delete_index(project['project_id'])
        for idx, eid in enumerate(eids):
            # update the progress status and save the status to disk
            status.progress = idx + 1
            status_service.save_status(query_id, status)

            # print progress
            print('processing entry ' + str(idx) + 'of ' + str(status.total) + ' entries: ' +
                  str(idx / status.total * 100) + '%')

            # retrieve data from scopus
            try:
                scopus_abstract = scopus.AbstractRetrieval(identifier=eid, id_type='eid', view="FULL", refresh=True)
            except IOError:
               print('could not collect data for EID ' + eid)
               missed_eids.append(eid)
               continue

            # create new AllResponses object to hold the individual information
            response = AllResponses(eid, project['name'], project['project_id'])

            # add scopus abstract to AllResponses object
            response.scopus_abstract_retrieval = scopus_abstract

            # get doi and collect unpaywall data and Altmetric data
            doi = scopus_abstract.doi
            if doi is not None:
                if doi is not "":
                    response.unpaywall_response = Unpaywall(doi)
                    response.altmetric_response = Altmetric(doi)
                    response.scival_data = Scival([])

            # send response to elastic search index
            elasticsearch_service.send_to_index(response, project['project_id'])
    eids_service.save_eid_list(project_id=project['project_id'], eids=missed_eids, prefix='missed_')

    status.status = "DATA_COLLECTED"
    status_service.save_status(query_id, status)
    project['isDataCollecting'] = False
    project['isDataCollected'] = True
    project_service.save_project(project)
    return Response({"status": "FINISHED"}, status=204)


@collector_blueprint.route('/collect_references/<query_id>', methods=['POST'])
def references_collection_execution(query_id):
    # initialize lists, read sample size from request and load eid list
    sample_size = int(request.args.get('sample_size'))
    missed_eids = []
    references_eids = []
    eids = eids_service.load_eid_list(query_id)

    # load project and set booleans
    project = project_service.load_project(query_id)
    project['isReferencesCollecting'] = True
    project['isReferencesCollected'] = False
    project_service.save_project(project)

    # prepare status
    status = Status("REFERENCES_COLLECTING")
    status.total = eids.__len__()
    status_service.save_status(query_id, status)

    # if eids are given, cycle through all of them
    if status.total > 0:
        for idx, eid in enumerate(eids):
            # update the progress status and save the status to disk
            status.progress = idx + 1
            status_service.save_status(query_id, status)

            # print progress
            print('processing entry ' + str(idx) + 'of ' + str(status.total) + ' entries: ' +
                  str(idx / status.total * 100) + '%')

            # retrieve refereces from scopus
            try:
                scopus_abstract = scopus.ScopusAbstract(eid, view="FULL")
                if scopus_abstract.references is not None:
                    references_eids = references_eids + scopus_abstract.references
                else:
                    print('no references given in scopus export.')
            except IOError:
                missed_eids.append(eid)
                continue
    # transform references eids into tuple and calculate the occurences
    references_eids_tuple = tuple(references_eids)
    occurences = Counter(references_eids_tuple)
    most_occurences = occurences.most_common(sample_size)

    # save the counter with the most occurences to disk
    counter_service.save_counter(query_id, most_occurences, 'references_')
    eids_service.save_eid_list(query_id, missed_eids, prefix='missed_')

    # set the status and save it to disk
    status.status = "DATA_COLLECTED"
    status_service.save_status(query_id, status)

    # set the project booleans and save it to disk
    project['isReferencesCollecting'] = False
    project['isReferencesCollected'] = True
    project_service.save_project(project)

    return Response({"status": "FINISHED"}, status=204)
