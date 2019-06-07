import json

from elasticsearch import Elasticsearch

from model import AllResponses
from model.UpdateContainer import UpdateContainer

es = Elasticsearch()


def send_to_index(all_responses: AllResponses, query_id):
    all_responses_json = json.dumps(all_responses, cls=PropertyEncoder)
    res = es.index(query_id, 'all_data', all_responses_json, all_responses.id, request_timeout=600)
    print('saved to index ' + query_id)
    return res


def append_to_index(document, eid, query_id):
    update_container = UpdateContainer(document)
    update_json = json.dumps(update_container, cls=HiddenEncoder)
    res = es.update(index=query_id, doc_type="all_data", id=eid, body=update_json)
    print('saved to index ' + query_id)
    return res


def delete_index(project_id):
    es.indices.delete(project_id, ignore=[400, 404])


class HiddenEncoder(json.JSONEncoder):
    def default(self, o):
        return_object = {}
        for key, value in o.__getstate__().items():
            if key.startswith('_'):
                return_object['key'.lstrip('_')] = value
        return return_object


class PropertyEncoder(json.JSONEncoder):
    def default(self, input_object):
        keys = dir(input_object)
        return_object = {}
        own_classes = ['AllResponses', 'Altmetric', 'Scival']
        object_type = type(input_object).__name__
        if object_type in own_classes:
            for key, value in input_object.__getstate__().items():
                return_object[key.lstrip('_')] = value
                continue
        elif object_type == 'Unpaywall':
            fields = ['doi', 'doi_resolver', 'evidence', 'free_fulltext_url', 'is_boai_license',
                      'is_free_to_read', 'is_subscription_journal', 'license', 'oa_color',
                      'reported_noncompliant_copies', 'title']
            for key in keys:
                if key in fields:
                    return_object[key] = getattr(input_object, key)
        elif object_type == 'AbstractRetrieval':
            fields = ['abstract', 'affiliation', 'authkeywords', 'authorgroup', 'authors', 'citedby-count',
                      'citedby-link', 'correspondence', 'coverDate', 'description', 'doi', 'eid', 'endingPage',
                      'funding', 'isbn', 'issn', 'identifier', 'idxterms', 'issueIdentifier',
                      'issuetitle', 'language', 'pageRange', 'publicationName', 'publisher', 'publisheraddress',
                      'refcount', 'references', 'scopus_link', 'self_link', 'source_id',
                      'sourcetitle_abbreviation', 'srctype', 'startingPage', 'subject_areas', 'url',
                      'volume', 'website', 'auid', 'indexed_name', 'surname', 'given_name', 'affiliation']
            for key in keys:
                if key in fields:
                    return_object[key] = getattr(input_object, key)
        elif object_type == '_ScopusAuthor':
            fields = ['indexed_name', 'given_name', 'surname', 'initials', 'author_url', 'auid', 'scopusid', 'seq']
            for key in keys:
                if key in fields:
                    return_object[key] = getattr(input_object, key)
        return return_object
