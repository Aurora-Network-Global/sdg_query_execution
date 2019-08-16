import scopus
from flask import Response, request, jsonify

from model.Query import Query
from model.Status import Status
from service import project_service, query_service, status_service, eids_service, relevance_measure_service
from . import query_blueprint


# retrieves a saved query from disk. If none is found, a new query is created and returned.
@query_blueprint.route("/single/<query_id>", methods=['GET'])
def get_query(query_id):
    try:
        query = query_service.load_query(query_id)
        return jsonify(query)
    except FileNotFoundError:
        query = Query()
        return jsonify(query.__dict__)


# retrieves the Scopus search string and to display it in the browser
@query_blueprint.route("/scopusSearchString/<query_id>", methods=['GET'])
def get_scopus_search_string(query_id):
    try:
        search_string = query_service.load_scopus_query(query_id)
        return Response(search_string, status=200)
    except FileNotFoundError:
        return Response("File not found", status=404)


# saves the query as json document in the working directory as query.json file. Creates a scopus search string and
# saves it as scopus_search_string.txt. Sets project.isQueryDefined = True
@query_blueprint.route("/single/<query_id>", methods=['POST'])
def save_query(query_id):
    project = project_service.load_project(query_id)
    query = request.get_json(silent=True)
    query_service.save_query(query_id, query)
    query_service.save_scopus_query(query_id, query)
    project['isQueryDefined'] = True
    project_service.save_project(project)
    return jsonify(query)


# executes the defined and saved query in scopus
@query_blueprint.route('/execution/<query_id>', methods=['POST'])
def query_execution(query_id):
    # reads the saved Scopus search string from disk
    search_string = query_service.load_scopus_query(query_id)

    # retrieve the project from disk, set the booleans and save the project
    project = project_service.load_project(query_id)
    project['isEidsCollected'] = False
    project['isEidsCollecting'] = True
    project_service.save_project(project)

    # prepares the status file
    status = Status("EIDS_COLLECTING")
    status_service.save_status(query_id, status)

    # perform the search in Scopus
    search = scopus.ScopusSearch(search_string, refresh=True, query_id=query_id)

    # retrieve the EIDs
    eids = []
    for result in search.results:
        eids.append(result.eid)

    # set the total number of results to the relevance_measures measure save it to disk
    relevance_measure = {'total_number_of_query_results': eids.__len__()}
    relevance_measure_service.save_relevance_measures(query_id, relevance_measure)

    # set the total number of results to the status save it to disk
    status.total = relevance_measure['total_number_of_query_results']
    status_service.save_status(query_id, status)

    # print the results to the command line for logging
    print('found ' + str(eids.__len__()) + ' in Scopus')

    # persist EIDs to file
    eids_service.save_eid_list(project_id=query_id, eids=eids)

    # set the status and save it to disk
    status = Status("EIDS_COLLECTED")
    status_service.save_status(query_id, status)

    # set the project boolean and save the project
    project['isEidslist'] = True
    project['isEidsCollected'] = True
    project['isEidsCollecting'] = False
    project_service.save_project(project)

    return Response({"status": "FINISHED"}, status=204)

