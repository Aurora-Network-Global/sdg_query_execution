import requests


class Altmetric:

    def __init__(self, api_key, doi):
        self.altmetric_url = "https://api.altmetric.com/v1"
        self.api_key = api_key
        url = self.altmetric_url + '/doi/' + doi + '?key=' + self.api_key
        r = requests.get(url)
        print("queryied URL: " + url + " with status code " + str(r.status_code))
        if r.status_code == 200:
            self.json = r.json()
            try:
                self._title = self.json['title']
            except KeyError:
                self._tile = None
            try:
                self._doi = self.json['doi']
            except KeyError:
                self._doi = None
            try:
                self._pmid = self.json['pmid']
            except KeyError:
                self._pmid = None
            try:
                self._tq = self.json['tq']
            except KeyError:
                self._tq = None
            try:
                self._uri = self.json['uri']
            except KeyError:
                self._uri = None
            try:
                self._altmetric_jid = self.json['altmetric_jid']
            except KeyError:
                self._altmetric_jid = None
            try:
                self._issns = self.json['issns']
            except KeyError:
                self._issns = None
            try:
                self._journal = self.json['journal']
            except KeyError:
                self._journal = None
            try:
                self._cohorts = self.json['cohorts']
            except KeyError:
                self._cohorts = None
            try:
                self._abstract = self.json['abstract']
            except KeyError:
                self._abstract = None
            try:
                self._abstract_source = self.json['abstract_source']
            except KeyError:
                self._abstract_source = None
            try:
                self._context = self.json['context']
            except KeyError:
                self._context = None
            try:
                self._authors = self.json['authors']
            except KeyError:
                self._authors = None
            try:
                self._type = self.json['type']
            except KeyError:
                self._type = None
            try:
                self._altmetric_id = self.json['altmetric_id']
            except KeyError:
                self._altmetric_id = None
            try:
                self._schema = self.json['schema']
            except KeyError:
                self._schema = None
            try:
                self._is_oa = self.json['is_oa']
            except KeyError:
                self._is_oa = None
            try:
                self._publisher_subjects = self.json['publisher_subjects']
            except KeyError:
                self._publisher_subjects = None
            try:
                self._cited_by_fbwalls_count = self.json['cited_by_fbwalls_count']
            except KeyError:
                self._cited_by_fbwalls_count = None
            try:
                self._cited_by_feeds_count = self.json['cited_by_feeds_count']
            except KeyError:
                self._cited_by_feeds_count = None
            try:
                self._cited_by_gplus_count = self.json['cited_by_gplus_count']
            except KeyError:
                self._cited_by_gplus_count = None
            try:
                self._cited_by_msm_count = self.json['cited_by_msm_count']
            except KeyError:
                self._cited_by_msm_count = None
            try:
                self._cited_by_policies_count = self.json['cited_by_policies_count']
            except KeyError:
                self._cited_by_policies_count = None
            try:
                self._cited_by_posts_count = self.json['cited_by_posts_count']
            except KeyError:
                self._cited_by_posts_count = None
            try:
                self._cited_by_rdts_count = self.json['cited_by_rdts_count']
            except KeyError:
                self._cited_by_rdts_count = None
            try:
                self._cited_by_tweeters_count = self.json['cited_by_tweeters_count']
            except KeyError:
                self._cited_by_tweeters_count = None
            try:
                self._cited_by_videos_count = self.json['cited_by_videos_count']
            except KeyError:
                self._cited_by_videos_count = None
            try:
                self._cited_by_wikipedia_count = self.json['cited_by_wikipedia_count']
            except KeyError:
                self._cited_by_wikipedia_count = None
            try:
                self._cited_by_patents_count = self.json['cited_by_patents_count']
            except KeyError:
                self._cited_by_patents_count = None
            try:
                self._cited_by_accounts_count = self.json['cited_by_accounts_count']
            except KeyError:
                self._cited_by_accounts_count = None
            try:
                self._last_updated = self.json['last_updated']
            except KeyError:
                self._last_updated = None
            try:
                self._score = self.json['score']
            except KeyError:
                self._score = None
            try:
                self._history = self.json['history']
            except KeyError:
                self._history = None
            try:
                self._url = self.json['url']
            except KeyError:
                self._url = None
            try:
                self._added_on = self.json['added_on']
            except KeyError:
                self._added_on = None
            try:
                self._published_on = self.json['published_on']
            except KeyError:
                self._published_on = None
            try:
                self._subjects = self.json['subjects']
            except KeyError:
                self._subjects = None
            try:
                self._scopus_subjects = self.json['scopus_subjects']
            except KeyError:
                self._scopus_subjects = None
            try:
                self._readers = self.json['readers']
            except KeyError:
                self._readers = None
            try:
                self._readers_count = self.json['readers_count']
            except KeyError:
                self._readers_count = None
            try:
                self._images = self.json['images']
            except KeyError:
                self._images = None
            try:
                self._details_url = self.json['details_url']
            except KeyError:
                self._details_url = None
        else:
            print(r.content)
    @property
    def title(self):
        return self._title

    @property
    def doi(self):
        return self._doi

    @property
    def pmid(self):
        return self._pmid

    @property
    def tq(self):
        return self._tq

    @property
    def uri(self):
        return self._uri

    @property
    def altmetric_jid(self):
        return self._altmetric_jid

    @property
    def issns(self):
        return self._issns

    @property
    def journal(self):
        return self._journal

    @property
    def cohorts(self):
        return self._cohorts

    @property
    def abstract(self):
        return self._abstract

    @property
    def abstract_source(self):
        return self._abstract_source

    @property
    def context(self):
        return self._context

    @property
    def authors(self):
        return self._authors

    @property
    def type(self):
        return self._type

    @property
    def altmetric_id(self):
        return self._altmetric_id

    @property
    def schema(self):
        return self._schema

    @property
    def is_oa(self):
        return self._is_oa

    @property
    def publisher_subjects(self):
        return self._publisher_subjects

    @property
    def cited_by_fbwalls_count(self):
        return self._cited_by_fbwalls_count

    @property
    def cited_by_feeds_count(self):
        return self._cited_by_feeds_count

    @property
    def cited_by_gplus_count(self):
        return self._cited_by_gplus_count

    @property
    def cited_by_msm_count(self):
        return self._cited_by_msm_count

    @property
    def cited_by_policies_count(self):
        return self._cited_by_policies_count

    @property
    def cited_by_posts_count(self):
        return self._cited_by_posts_count

    @property
    def cited_by_rdts_count(self):
        return self._cited_by_rdts_count

    @property
    def cited_by_tweeters_count(self):
        return self._cited_by_tweeters_count

    @property
    def cited_by_videos_count(self):
        return self._cited_by_videos_count

    @property
    def cited_by_wikipedia_count(self):
        return self._cited_by_wikipedia_count

    @property
    def cited_by_patents_count(self):
        return self._cited_by_patents_count

    @property
    def cited_by_accounts_count(self):
        return self._cited_by_accounts_count

    @property
    def last_updated(self):
        return self._last_updated

    @property
    def score(self):
        return self._score

    @property
    def history(self):
        return self._history

    @property
    def url(self):
        return self._url

    @property
    def added_on(self):
        return self._added_on

    @property
    def published_on(self):
        return self._published_on

    @property
    def subjects(self):
        return self._subjects

    @property
    def scopus_subjects(self):
        return self._scopus_subjects

    @property
    def readers(self):
        return self._readers

    @property
    def readers_count(self):
        return self._readers_count

    @property
    def images(self):
        return self._images

    @property
    def details_url(self):
        return self._details_url

    def __getstate__(self):
        state = self.__dict__.copy()
        try:
            del state['json']
        except KeyError:
            print('no JSON data')
        del state['api_key']
        del state['altmetric_url']
        return state
