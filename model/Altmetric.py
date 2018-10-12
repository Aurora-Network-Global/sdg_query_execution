import requests
import hashlib

from utilities import utils


class Altmetric:

    def __init__(self, key):
        self.altmetric_url = "https://api.altmetric.com/v1"
        self.api_key = key
        self.secret = ""

    def set_secret(self, secret):
        self.secret = secret

    def get_data_for_doi(self, doi):
        url = self.altmetric_url + '/doi/' + doi + '?key=' + self.api_key
        r = requests.get(url)
        print("queryied URL: " + url + " with status code " + str(r.status_code))
        if r.status_code == 200:
            return r.json()
        else:
            return None

    # def get_data_for_query(self, query):
        # filters = utils.convert_search_to_altmetric_seach_string(query)
        # digest = hashlib.sha1()
        # first_digest = digest.sha1(filters)
        # second_digest = first_digest.update(self.secret)
        # hash = second_digest.hexdigest()
