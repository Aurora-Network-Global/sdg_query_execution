################
#    imports   #
################

import json

from flask import Response, request, jsonify
from pybliometrics import scopus

from model.RelevanceMeasures import RelevanceMeasure
from model.Status import Status
from query.Query import Query
from query.QueryDefinitions import QueryDefinitions
from service import project_service, query_service, status_service, eids_service, relevance_measure_service
from . import query_blueprint


################
#    routes    #
################

@query_blueprint.route("/single/<project_id>", methods=['GET'])
def get_query(project_id):
    """
    retrieves a saved query from disk. If none is found, a new query is created and returned.
    :param project_id: the ID of the current project
    :return: the query saved on disk. If none is found, a new, empty query is returned
    """
    print("showing query for project {}".format(project_id))
    try:
        query = query_service.load_query_from_xml(project_id)
    except FileNotFoundError:
        try:
            query = query_service.import_old_query(project_id)
            query_service.save_query_to_xml(project_id, query)
        except FileNotFoundError:
            query_definitions = QueryDefinitions()
            query = Query(query_definitions=query_definitions)
    return json.dumps(query.__getstate__(), default=lambda o: o.__getstate__())


@query_blueprint.route("/single_xml/<project_id>", methods=['GET'])
def get_xml_query(project_id):
    """
    retrieves a saved query from disk. If none is found, a new query is created and returned.
    :param project_id: the ID of the current project
    :return: a query in XML format is retrieved from disc. If none is found a status of 404 is returned.
    """
    try:
        query = query_service.load_query_from_xml(project_id)
        return json.dumps(query.__getstate__(), default=lambda o: o.__getstate__())
    except FileNotFoundError:
        return Response("File not found", status=404)


@query_blueprint.route("/scopusSearchString/<project_id>", methods=['GET'])
def get_scopus_search_string(project_id):
    """
    retrieves the Scopus search string and to display it in the browser
    :param project_id: the ID of the current project
    :return: returns the scopus query strings. if no scopus queries are found, a status of 404 is returned.
    """
    try:
        scopus_queries = query_service.load_scopus_queries(project_id)
        return json.dumps(scopus_queries, default=lambda o: o.__getstate__())
    except FileNotFoundError:
        return Response("File not found", status=404)


@query_blueprint.route("/scopusQueriesFromXml/<project_id>", methods=['GET'])
def get_scopus_search_string_from_xml(project_id):
    """
    retrieves the Scopus search string and to display it in the browser
    :param project_id: the ID of the current project
    :return: the overall scopus search string. if no scopus queries are found, a status of 404 is returned.
    """
    try:
        scopus_queries = query_service.load_scopus_query_from_xml(project_id)
        return scopus_queries.overall
    except FileNotFoundError:
        return Response("File not found", status=404)


@query_blueprint.route("/single_xml/<project_id>", methods=['POST'])
def save_query_as_xml(project_id):
    """
    saves the query as xml document in the working directory as query.json file. Creates a scopus search string and
    saves it as scopus_search_string.txt. Sets project.isQueryDefined = True
    :param project_id: the ID of the current project
    :return: the saved query
    """
    project = project_service.load_project(project_id)
    query_json = request.get_json(silent=True)
    query = query_service.from_json(query_json)
    try:
        query_service.save_query_to_xml(project_id, query)
    except IOError:
        return Response("could not save query", status=500)
    query_service.create_scopus_queries(project_id, query)
    project.isQueryDefined = True
    project_service.save_project(project)
    return json.dumps(query, default=lambda o: o.__getstate__())


@query_blueprint.route('/execution/<project_id>', methods=['POST'])
def query_execution(project_id):
    """
    executes the defined and saved query in scopus
    :param project_id: the ID of the current project
    :return: 'finished' with a status of 204 when the query was executed successfully
    """
    print('running project {}'.format(project_id))
    # reads the saved Scopus search string from disk
    scopus_queries = query_service.load_scopus_queries(project_id)

    # retrieve the project from disk, set the booleans and save the project
    project = project_service.load_project(project_id)
    project.isEidsCollected = False
    project.isEidsCollecting = True
    project_service.save_project(project)

    # prepares the status file
    status = Status("EIDS_COLLECTING")
    status_service.save_status(project_id, status)

    # prepare EIDs list
    eids = []

    for search_string in scopus_queries.search_strings:
        print('executing search {}'.format(search_string))
        search = scopus.ScopusSearch(search_string, refresh=True)
        print(search)
        for result in search.results:
            # add EID if it is not already in the list (from a former search)
            eids.append(result.eid)

    # convert to set in order to remove duplicates
    eids = set(eids)

    # set the total number of results to the relevance_measures measure save it to disk
    relevance_measure = RelevanceMeasure(number_of_search_results=eids.__len__())
    relevance_measure_service.save_relevance_measures(project_id, relevance_measure)

    # set the total number of results to the status save it to disk
    status.total = relevance_measure.number_of_search_results
    status_service.save_status(project_id, status)

    # print the results to the command line for logging
    print('found ' + str(eids.__len__()) + ' in Scopus')

    # persist EIDs to file
    eids_service.save_eid_list(project_id=project_id, eids=eids)

    # set the status and save it to disk
    status = Status("EIDS_COLLECTED")
    status_service.save_status(project_id, status)

    # set the project boolean and save the project
    project.isEidslist = True
    project.isEidsCollected = True
    project.isEidsCollecting = False
    project_service.save_project(project)

    return Response({"status": "FINISHED"}, status=204)

