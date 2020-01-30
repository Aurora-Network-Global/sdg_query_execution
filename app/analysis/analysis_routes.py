################
#    imports   #
################

import json

import numpy as np
from elasticsearch import Elasticsearch
from flask import Response, request

from model.AbstractText import AbstractText
from service import project_service
from utilities.utils import calculate_symmetric_overlap, calculate_asymmetric_overlap
from flask import current_app as app
from . import analysis_blueprint

es = Elasticsearch()


################
#    routes    #
################

@analysis_blueprint.route('/prepare_abstracts/<project_id>', methods=['POST'])
def count_keywords(project_id):
    """
    returns a list of abstracts contained in the project
    :param project_id: the ID of the current project
    :return: a JSON formatted list of the abstracts
    """
    project = project_service.load_project(project_id)
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
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


# @app.route("/calculateTextrank/<project_id>")
# def calculate_text_rank(project_id):
#     path_to_file = location + '/out/' + project_id + '/abstracts.json'
#     for graf in pytextrank.parse_doc(pytextrank.json_iter(path_to_file)):
#         print(pytextrank.pretty_print(graf))
#     return "ok"

@analysis_blueprint.route('/analysis/overlap', methods=['GET'])
def calculate_overlap():
    """
    calculates the overlap between two query. The indivudial query IDs are provided as path variables 'primary' and
    'secondary
    :return: Response status 200 if the calculation succeeded.
    """
    print('calculating overview')
    list_ids = request.args.getlist('primary')
    second_list = request.args.getlist('secondary')
    if second_list.__len__() == 0:
        array = calculate_symmetric_overlap(list_ids)
        length_func = np.vectorize(get_length)
        return Response({"status": "FINISHED"}, status=200)
    else:
        calculate_asymmetric_overlap(list_ids, second_list)
        return Response({"status": "FINISHED"}, status=200)


def get_length(x):
    if x is not None:
        return len(x)
    else:
        return 0


