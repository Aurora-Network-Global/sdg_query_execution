import json

from elasticsearch import Elasticsearch

from model import AllResponses
from model.Survey import Survey
from model.UpdateContainer import UpdateContainer
from flask import current_app as app

es = Elasticsearch('localhost:9200')


def send_to_index(all_responses: AllResponses, project_id):
    try:
        all_responses_json = json.dumps(all_responses, cls=PropertyEncoder)
        res = es.index(project_id, 'all_data', all_responses_json, all_responses.id, request_timeout=600)
        app.logger.info('saved to index ' + project_id)
    except Exception as exception:
        app.logger.error('could not save {} to elasticsearch, reason: {}'.format(all_responses.id, exception.with_traceback()))
        return None
    return res


def save_survey(survey: Survey):
    index = 'survey_' + survey.project_id + '_' + survey.survey_id
    for result in survey.survey_results:
        survey_json = json.dumps(result, cls=HiddenEncoder)
        res = es.index(index, 'all_data', survey_json, result.session, request_timeout=600)
    print('saved to index ' + index)
    return res


def get_number_of_records(project_id):
    es.indices.refresh(project_id)
    return es.cat.count(project_id, params={"format": "json"})[0]['count']


def append_to_index(document, eid, project_id):
    update_container = UpdateContainer(document)
    update_json = json.dumps(update_container, cls=HiddenEncoder)
    try:
        res = es.update(index=project_id, doc_type="all_data", id=eid, body=update_json)
        return res
    except:
        print('could not send scival update')


def save_survey_judgement(judgement, project_id):
    try:
        update = '{"doc": { "accepted": ' + str(judgement['judgement']).lower() + '}}'
        print(update)
        res = es.update(index=project_id, doc_type="all_data", id=judgement['eid'], body=update)
        return res
    except:
        print('could not send scival update')


def delete_index(project_id):
    es.indices.delete(project_id, ignore=[400, 404])


def delete_survey_index(survey):
    es.indices.delete('survey_' + survey.project_id, ignore=[400, 404])


class HiddenEncoder(json.JSONEncoder):
    def default(self, o):
        return_object = {}
        for key, value in o.__getstate__().items():
            if key.startswith('_'):
                return_object[key.lstrip('_')] = value
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
                    try:
                        return_object[key] = getattr(input_object, key)
                    except TypeError:
                        print('could not save key: ' + key)
        elif object_type == '_ScopusAuthor':
            fields = ['indexed_name', 'given_name', 'surname', 'initials', 'author_url', 'auid', 'scopusid', 'seq']
            for key in keys:
                if key in fields:
                    return_object[key] = getattr(input_object, key)
        return return_object
