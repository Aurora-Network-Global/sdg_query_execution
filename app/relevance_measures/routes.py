#################
#### imports ####
#################
from model.RelevanceMeasures import RelevanceMeasure
from service import eids_service, project_service, relevance_measure_service
from . import relevance_measures_blueprint
from flask import current_app as app, jsonify, Response


################
#### routes ####
################

# check the provided test EIDs vs the obtained result set
@relevance_measures_blueprint.route("/relevanceMeasures/getRecall/<query_id>", methods=['GET'])
def check_test_eids(query_id):
    test_eids = eids_service.load_eid_list(query_id, 'test_')

    # load collected eids
    eids = eids_service.load_eid_list(query_id)
    relevance_measure = relevance_measure_service.load_relevance_measure(query_id)
    if relevance_measure is None:
        relevance_measure = RelevanceMeasure()
    relevance_measure['number_of_search_results'] = eids.__len__()
    relevance_measure['number_test_entries'] = test_eids.__len__()
    relevance_measure['number_test_entries_found'] = 0
    for test_eid in test_eids:
        if test_eid in eids:
            relevance_measure['number_test_entries_found'] = relevance_measure['number_test_entries_found'] + 1
    if relevance_measure['number_of_search_results'] > 0:
        relevance_measure['recall'] = relevance_measure['number_test_entries_found'] / relevance_measure['number_test_entries']
    else:
        relevance_measure['recall'] = 0
    relevance_measure_service.save_relevance_measures(query_id, relevance_measure)
    return jsonify(relevance_measure)

# reads the relavance measures file (relevance_measures.json) and returns it.
@relevance_measures_blueprint.route("/relevanceMeasures/single/<query_id>")
def get_relevance_measures(query_id):
    try:
        relevance_measure = relevance_measure_service.load_relevance_measure(query_id)
        return jsonify(relevance_measure)
    except FileNotFoundError:
        return Response("File not found", status=404)


# check the provided test EIDs vs the obtained result set
@relevance_measures_blueprint.route("/relevanceMeasures/getPrecision/<query_id>", methods=['GET'])
def getPrecision(query_id):
    # load collected eids
    eids = eids_service.load_eid_list(query_id)
    relevance_measure = relevance_measure_service.load_relevance_measure(query_id)
    if relevance_measure is None:
        relevance_measure = RelevanceMeasure()
    relevance_measure['number_of_search_results'] = eids.__len__()
    judgement_list = eids_service.load_judgement_file(query_id)
    relevance_measure['number_sample_entries'] = judgement_list.__len__()
    relevance_measure['number_positive_sample_entries'] = 0
    for judgement in judgement_list:
        if judgement['isRelevant']:
            relevance_measure['number_positive_sample_entries'] = \
                relevance_measure['number_positive_sample_entries'] + 1
    if relevance_measure['number_sample_entries'] > 0:
        relevance_measure['precision'] = relevance_measure['number_positive_sample_entries'] / relevance_measure['number_sample_entries']
    else:
        relevance_measure['precision'] = 0
    relevance_measure_service.save_relevance_measures(query_id, relevance_measure)
    return jsonify(relevance_measure)
