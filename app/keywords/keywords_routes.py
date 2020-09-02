################
#    imports   #
################

import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from flask import Response
from flask import current_app as app

from . import keywords_blueprint

es = Elasticsearch()


################
#    routes    #
################

@keywords_blueprint.route("/collect/<project_id>")
def get_keywords(project_id):
    """
    retrieve the list of keywords for the search
    :param project_id: the ID of the current project
    :return:
    """
    try:
        search = es.search(index=project_id, doc_type='all_data', size=1000, scroll='3m')
    except IOError:
        return Response('no keywords ', status=404)
    sid = search['_scroll_id']
    scroll_size = search['hits']['total']
    fields = {'abstract': None}
    append_results_to_fields(fields, search)
    while scroll_size > 0:
        page = es.scroll(scroll_id=sid, scroll='3m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])
        append_results_to_fields(fields, page)
    elastic_df = pd.DataFrame.from_dict(fields)
    print(elastic_df['abstract'])
    return Response('success ', status=200)


def append_results_to_fields(fields, search):
    interesting_fields = ['abstract']
    for hit in search["hits"]["hits"]:
        for interesting_field in interesting_fields:
            try:
                fields[interesting_field] = np.append(fields[interesting_field],
                                                      hit['_source']['scopus_abstract_retrieval'][interesting_field])
            except KeyError:
                fields[interesting_field] = np.append(fields[interesting_field], '')
