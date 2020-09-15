#################
#    imports    #
#################

from collections import Counter
import math
from flask import Response, request, current_app as app
from pybliometrics import scopus

from threading import Thread

from altmetric.Altmetric import Altmetric
from model.AllResponses import AllResponses
from model.Status import Status
from scival.Scival import Scival
from service import project_service, status_service, eids_service, \
    elasticsearch_service, counter_service
from unpaywall.Unpaywall import Unpaywall
from . import collector_blueprint


################
#    routes    #
################


@collector_blueprint.route('/collect_data/<project_id>', methods=['POST'])
def data_collection_execution(project_id):
    """
    run the data collection

    :parameter project_id the id of the current project

    """

    mode = ''

    if request.args.get('mode') is not None:
        mode = request.args.get('mode')

    app.logger.info('project {}: collecting data with mode {}'.format(project_id, mode))

    # load project, set status bools, and load and eid list. initialize missed eid list
    project = project_service.load_project(project_id)
    project.isDataCollecting = True
    project.isDataCollected = False
    eids = eids_service.load_eid_list(project_id, mode)
    missed_eids = []

    with app.app_context():
        keys = app.config.get("LIBINTEL_SCOPUS_KEYS")

    # initialize status, set to collecting and save status
    status = Status("DATA_COLLECTING")
    status.total = len(eids)
    status_service.save_status(project_id, status)

    if status.total > 0:
        if mode != 'missed':
            elasticsearch_service.delete_index(project.project_id)
        else:
            eids_service.deleteMissedEids()
        if type(keys) is tuple:

            # the number of threads is given by the number of available API keys
            number_of_threads = len(keys)
            app.logger.info('project {}: collecting data in {} threads'.format(project_id, number_of_threads))

            # gather the individual chunks provided to each process
            length_of_chunks = math.ceil(status.total / number_of_threads)
            list_chunks = list(chunks(eids, length_of_chunks))

            # make asynchronous calls and delegate the individual collection to the individual threads
            for key_index, key in enumerate(keys):
                thread = Thread(target=collect_data, args=(list_chunks[key_index], project.project_id, project.name, key_index, key,
                                  app._get_current_object()))
                thread.start()
            return Response('finished', status=204)

        collect_data(eids=eids, project_id=project.project_id, project_name=project.name, i=0, key=keys, app=app._get_current_object())

        # if only one API-Key is given, collect data sequentially
        for idx, eid in enumerate(eids):

            # set scopus api-key to the provided key
            scopus.config['Authentication']['APIKEy'] = keys

            # update the progress status and save the status to disk
            status.progress = idx + 1
            status_service.save_status(project_id, status)

            # print progress
            app.logger.info('project {}: processing entry ' + str(idx) + 'of ' + str(status.total) + ' entries: ' +
                  str(idx / status.total * 100) + '%')

            # retrieve data from scopus
            try:
                scopus_abstract = scopus.AbstractRetrieval(identifier=eid, id_type='eid', view="FULL", refresh=True)
                app.logger.info('project {}: collected scopus data for EID {}'.format(project_id, eid))
            except Exception as inst:
                app.logger.error('project {}: could not collect scopus data for EID {}, exception: {}'.format(project_id, eid, type(inst)))
                missed_eids.append(eid)
                continue

            # create new AllResponses object to hold the individual information
            response = AllResponses(eid, project.name, project.project_id)

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
            elasticsearch_service.send_to_index(response, project.project_id)
            app.logger.info('project {}: saved EID {} to elasticsearch'.format(project_id, eid))
    eids_service.save_eid_list(project_id=project.project_id, eids=missed_eids, prefix='missed_')
    app.logger.info('project {}: all EID data collected'.format(project_id))
    status.status = "DATA_COLLECTED"
    status_service.save_status(project_id, status)
    project.isDataCollecting = False
    project.isDataCollected = True
    project_service.save_project(project)
    return Response({"status": "FINISHED"}, status=204)



# cuts lists into chunks
# Thanks to Ned Batchelder on Stack overflow (https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks)
def chunks(l, n):
    """Yield successive n-sized chunks from list l
    :parameter l inital lists
    :parameter n number of chunks

    returns an array of arrays
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def collect_data(eids, project_id, project_name, i, key, app):
    """collects the data for a provided list of eids and stores them into a elasticsearch
    function to be called upon parrallization.

    :parameter eids list of EIDs
    :parameter project_id the ID of the current project
    :parameter project_name the name of the current project
    :parameter i the index of the API-key being used
    :parameter key the API-key value to be used
    :parameter app the app object to retrieve the context from
    """
    with app.app_context():
        scopus.config['Authentication']['APIKEy'] = key
        missed_eids = []
        for idx, eid in enumerate(eids):

            # retrieve data from scopus
            try:
                scopus_abstract = scopus.AbstractRetrieval(identifier=eid, id_type='eid', view="FULL", refresh=True)
                app.logger.info('project {}: collected scopus data for EID {}'.format(project_id, eid))
            except:
                app.logger.error('project {}: could not collect scopus data for EID {}'.format(project_id, eid))
                missed_eids.append(eid)
                continue

            # create new AllResponses object to hold the individual information
            response = AllResponses(eid, project_name, project_id=project_id)

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
            elasticsearch_service.send_to_index(response, project_id)
            app.logger.info('project {}: saved EID {} to elasticsearch'.format(project_id, eid))
        eids_service.save_eid_list(project_id=project_id, eids=missed_eids, prefix=(str(i) + '_missed_'))
        app.logger.info('project {}: saved {} missed EIDs'.format(project_id, len(missed_eids)))


@collector_blueprint.route('/collect_references/<project_id>', methods=['POST'])
def references_collection_execution(project_id):
    """
    collects the references for a given collection of publications
    :param project_id: the ID of the current project
    :return: 204 if successful
    """
    # initialize lists, read sample size from request and load eid list
    sample_size = int(request.args.get('sample_size'))
    missed_eids = []
    references_eids = []
    eids = eids_service.load_eid_list(project_id)

    # load project and set booleans
    project = project_service.load_project(project_id)
    project.isReferencesCollecting = True
    project.isReferencesCollected = False
    project_service.save_project(project)

    # prepare status
    status = Status("REFERENCES_COLLECTING")
    status.total = eids.__len__()
    status_service.save_status(project_id, status)

    # if eids are given, cycle through all of them
    if status.total > 0:
        for idx, eid in enumerate(eids):
            # update the progress status and save the status to disk
            status.progress = idx + 1
            status_service.save_status(project_id, status)

            # print progress
            app.logger.info('project {}: processing entry ' + str(idx) + 'of ' + str(status.total) + ' entries: ' +
                            str(idx / status.total * 100) + '%')

            # retrieve refereces from scopus
            try:
                scopus_abstract = scopus.AbstractRetrieval(eid, view="FULL")
                app.logger.info('project {}: collected scopus data for EID {}'.format(project_id, eid))
                if scopus_abstract.references is not None:
                    references_eids = references_eids + scopus_abstract.references
                else:
                    app.logger.warn('project {}: no references given in scopus export for EID {}.'.format(project_id, eid))
            except IOError:
                app.logger.error('project {}: could not collect scopus data for EID {}'.format(project_id, eid))
                missed_eids.append(eid)
                continue
    # transform references eids into tuple and calculate the occurences
    references_eids_tuple = tuple(references_eids)
    occurences = Counter(references_eids_tuple)
    most_occurences = occurences.most_common(sample_size)

    # save the counter with the most occurences to disk
    counter_service.save_counter(project_id, most_occurences, 'references_')
    eids_service.save_eid_list(project_id, missed_eids, prefix='missed_')

    # set the status and save it to disk
    status.status = "DATA_COLLECTED"
    status_service.save_status(project_id, status)

    # set the project booleans and save it to disk
    project.isReferencesCollecting = False
    project.isReferencesCollected = True
    project_service.save_project(project)

    return Response({"status": "FINISHED"}, status=204)
