#################
#    imports    #
#################

import json

from model.RelevanceMeasures import RelevanceMeasure
from service import eids_service, relevance_measure_service
from . import relevance_measures_blueprint
from flask import jsonify, Response
from flask import current_app as app


################
#    routes    #
################

# check the provided test EIDs vs the obtained result set
@relevance_measures_blueprint.route("/relevanceMeasures/getRecall/<project_id>", methods=['GET'])
def check_test_eids(project_id):
    """
    calcluates the Recall by comparing the list of EIDs retrieved from the query against lists of EIDs as obtained from
     the survey
    :param project_id: the ID of the current project
    :return: a JSON formatted relevance measure object.
    """
    test_eids = eids_service.load_eid_list(project_id, 'test_')
    app.logger.info('project {}: loaded test eids'.format(project_id))

    # load collected eids
    eids = eids_service.load_eid_list(project_id)
    relevance_measure = relevance_measure_service.load_relevance_measure(project_id)
    if relevance_measure is None:
        relevance_measure = RelevanceMeasure()
    relevance_measure.number_of_search_results = len(eids)
    relevance_measure.number_test_entries = len(test_eids)
    relevance_measure.number_test_entries_found = 0
    for test_eid in test_eids:
        if test_eid in eids:
            relevance_measure.number_test_entries_found = relevance_measure.number_test_entries_found + 1
    if relevance_measure.number_of_search_results > 0:
        relevance_measure.recall = relevance_measure.number_test_entries_found / relevance_measure.number_test_entries
    else:
        relevance_measure.recall = 0
    relevance_measure_service.save_relevance_measures(project_id, relevance_measure)
    app.logger.info('project {}: calculated relevance measure recall'.format(project_id))
    return jsonify(relevance_measure)


# reads the relavance measures file (relevance_measures.json) and returns it.
@relevance_measures_blueprint.route("/relevanceMeasures/single/<project_id>")
def get_relevance_measures(project_id):
    """

    :param project_id:
    :return:
    """
    try:
        relevance_measure = relevance_measure_service.load_relevance_measure(project_id)
        app.logger.info('project {}: loaded relevance measures'.format(project_id))
        return json.dumps(relevance_measure, default=lambda o: o.__getstate__())
    except FileNotFoundError:
        return Response("File not found", status=404)


# check the provided test EIDs vs the obtained result set
@relevance_measures_blueprint.route("/relevanceMeasures/getPrecision/<project_id>", methods=['GET'])
def getPrecision(project_id):
    # load collected eids
    eids = eids_service.load_eid_list(project_id)
    relevance_measure = relevance_measure_service.load_relevance_measure(project_id)
    if relevance_measure is None:
        relevance_measure = RelevanceMeasure()
    relevance_measure.number_of_search_results = len(eids)
    judgement_list = eids_service.load_judgement_file(project_id)
    app.logger.info('project {}: loaded judgements'.format(project_id))
    relevance_measure.number_sample_entries = len(judgement_list)
    relevance_measure.number_positive_sample_entries = 0
    for judgement in judgement_list:
        if judgement.isRelevant:
            relevance_measure.number_positive_sample_entries = \
                relevance_measure.number_positive_sample_entries + 1
    if relevance_measure.number_sample_entries > 0:
        relevance_measure.precision = relevance_measure.number_positive_sample_entries / relevance_measure.number_sample_entries
    else:
        relevance_measure.precision = 0
    relevance_measure_service.save_relevance_measures(project_id, relevance_measure)
    app.logger.info('project {}: calculated relevance measure precision'.format(project_id))
    return jsonify(relevance_measure)
