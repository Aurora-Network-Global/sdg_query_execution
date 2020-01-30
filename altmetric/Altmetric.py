import requests

from flask import current_app as app


class Altmetric:
    """A class representing the results when querying the altmetric API.
    Currently only the free API is supported but further support will be implemented. """

    def __init__(self, doi):
        with app.app_context():
            api_key = app.config.get("ALTMETRIC_API_KEY")
            secret = app.config.get("ALTMETRIC_API_SECRET")

        self.altmetric_url = "https://api.altmetric.com/v1"
        self.api_key = api_key
        url = self.altmetric_url + '/doi/' + doi # + '?key=' + self.api_key
        r = requests.get(url)
        # print("queryied URL: " + url + " with status code " + str(r.status_code))
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
            self._tile = None
            self._doi = None
            self._pmid = None
            self._tq = None
            self._uri = None
            self._altmetric_jid = None
            self._issns = None
            self._journal = None
            self._cohorts = None
            self._abstract = None
            self._abstract_source = None
            self._context = None
            self._authors = None
            self._type = None
            self._altmetric_id = None
            self._schema = None
            self._is_oa = None
            self._publisher_subjects = None
            self._cited_by_fbwalls_count = None
            self._cited_by_feeds_count = None
            self._cited_by_gplus_count = None
            self._cited_by_msm_count = None
            self._cited_by_policies_count = None
            self._cited_by_posts_count = None
            self._cited_by_rdts_count = None
            self._cited_by_tweeters_count = None
            self._cited_by_videos_count = None
            self._cited_by_wikipedia_count = None
            self._cited_by_patents_count = None
            self._cited_by_accounts_count = None
            self._last_updated = None
            self._score = None
            self._history = None
            self._url = None
            self._added_on = None
            self._published_on = None
            self._subjects = None
            self._scopus_subjects = None
            self._readers = None
            self._readers_count = None
            self._images = None
            self._details_url = None
    @property
    def title(self):
        try:
            return self._title
        except AttributeError:
            return None

    @property
    def doi(self):
        try:
            return self._doi
        except AttributeError:
            return None

    @property
    def pmid(self):
        try:
            return self._pmid
        except AttributeError:
            return None

    @property
    def tq(self):
        try:
            return self._tq
        except AttributeError:
            return None

    @property
    def uri(self):
        try:
            return self._uri
        except AttributeError:
            return None

    @property
    def altmetric_jid(self):
        try:
            return self._altmetric_jid
        except AttributeError:
            return None

    @property
    def issns(self):
        try:
            return self._issns
        except AttributeError:
            return None

    @property
    def journal(self):
        try:
            return self._journal
        except AttributeError:
            return None

    @property
    def cohorts(self):
        try:
            return self._cohorts
        except AttributeError:
            return None

    @property
    def abstract(self):
        try:
            return self._abstract
        except AttributeError:
            return None

    @property
    def abstract_source(self):
        try:
            return self._abstract_source
        except AttributeError:
            return None

    @property
    def context(self):
        try:
            return self._context
        except AttributeError:
            return None

    @property
    def authors(self):
        try:
            return self._authors
        except AttributeError:
            return None

    @property
    def type(self):
        try:
            return self._type
        except AttributeError:
            return None

    @property
    def altmetric_id(self):
        try:
            return self._altmetric_id
        except AttributeError:
            return None

    @property
    def schema(self):
        try:
            return self._schema
        except AttributeError:
            return None

    @property
    def is_oa(self):
        try:
            return self._is_oa
        except AttributeError:
            return None

    @property
    def publisher_subjects(self):
        try:
            return self._publisher_subjects
        except AttributeError:
            return None

    @property
    def cited_by_fbwalls_count(self):
        try:
            return self._cited_by_fbwalls_count
        except AttributeError:
            return None

    @property
    def cited_by_feeds_count(self):
        try:
            return self._cited_by_feeds_count
        except AttributeError:
            return None

    @property
    def cited_by_gplus_count(self):
        try:
            return self._cited_by_gplus_count
        except AttributeError:
            return None

    @property
    def cited_by_msm_count(self):
        try:
            return self._cited_by_msm_count
        except AttributeError:
            return None

    @property
    def cited_by_policies_count(self):
        try:
            return self._cited_by_policies_count
        except AttributeError:
            return None

    @property
    def cited_by_posts_count(self):
        try:
            return self._cited_by_posts_count
        except AttributeError:
            return None

    @property
    def cited_by_rdts_count(self):
        try:
            return self._cited_by_rdts_count
        except AttributeError:
            return None

    @property
    def cited_by_tweeters_count(self):
        try:
            return self._cited_by_tweeters_count
        except AttributeError:
            return None

    @property
    def cited_by_videos_count(self):
        try:
            return self._cited_by_videos_count
        except AttributeError:
            return None

    @property
    def cited_by_wikipedia_count(self):
        try:
            return self._cited_by_wikipedia_count
        except AttributeError:
            return None

    @property
    def cited_by_patents_count(self):
        try:
            return self._cited_by_patents_count
        except AttributeError:
            return None

    @property
    def cited_by_accounts_count(self):
        try:
            return self._cited_by_accounts_count
        except AttributeError:
            return None

    @property
    def last_updated(self):
        try:
            return self._last_updated
        except AttributeError:
            return None

    @property
    def score(self):
        try:
            return self._score
        except AttributeError:
            return None

    @property
    def history(self):
        try:
            return self._history
        except AttributeError:
            return None

    @property
    def url(self):
        try:
            return self._url
        except AttributeError:
            return None

    @property
    def added_on(self):
        try:
            return self._added_on
        except AttributeError:
            return None

    @property
    def published_on(self):
        try:
            return self._published_on
        except AttributeError:
            return None

    @property
    def subjects(self):
        try:
            return self._subjects
        except AttributeError:
            return None

    @property
    def scopus_subjects(self):
        try:
            return self._scopus_subjects
        except AttributeError:
            return None

    @property
    def readers(self):
        try:
            return self._readers
        except AttributeError:
            return None

    @property
    def readers_count(self):
        try:
            return self._readers_count
        except AttributeError:
            return None

    @property
    def images(self):
        try:
            return self._images
        except AttributeError:
            return None

    @property
    def details_url(self):
        try:
            return self._details_url
        except AttributeError:
            return None

    def __getstate__(self):
        state = self.__dict__.copy()
        try:
            del state['json']
        except KeyError:
            print('no Altmetric data found data')
        del state['api_key']
        del state['altmetric_url']
        return state
