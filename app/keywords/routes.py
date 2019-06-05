import json

from elasticsearch import Elasticsearch
from flask import Response

from utilities import utils
from . import keywords_blueprint

es = Elasticsearch()

# retrieve the list of keywords for the search
@keywords_blueprint.route("/collect/<query_id>")
def get_keywords(query_id):
    try:
        page = es.search(index=query_id, doc_type='all_data', size=1000, scroll='3m')
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']
        keyword_list = []
        for hit in page["hits"]["hits"]:
            try:
                keyword_list.extend(hit["_source"]["scopus_abtract_retrieval"]["authkeywords"])
            except KeyError:
                print('no keywords given')
        while (scroll_size > 0):
            page = es.scroll(scroll_id=sid, scroll='3m')
            sid = page['_scroll_id']
            scroll_size = len(page['hits']['hits'])
            for hit in page["hits"]["hits"]:
                try:
                    keyword_list.extend(hit["_source"]["scopus_abtract_retrieval"]["authkeywords"])
                except KeyError:
                    print('no keywords given')
        dictionary = utils.wordlist_to_freq_dict(keyword_list)
        sorted_dict = utils.sort_freq_dict(dictionary)
        return json.dumps([ob.__dict__ for ob in sorted_dict])
    except IOError:
        return Response('no keywords ', status=404)
