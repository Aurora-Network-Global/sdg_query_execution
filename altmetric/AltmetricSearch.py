import requests
import hashlib

from utilities import utils


class AltmetricSearch:

    def __init__(self, api_key, secret, query):
        self.altmetric_url = "https://api.altmetric.com/v1"
        self.api_key = api_key
        self.secret = secret

        filters = utils.convert_search_to_altmetric_seach_string(query)
        digest = hashlib.sha1()
        first_digest = digest.sha1(filters)
        second_digest = first_digest.update(self.secret)
        filter_hash = second_digest.hexdigest()
        url = self.altmetric_url + '/doi/' + filter_hash + '?key=' + self.api_key
        r = requests.get(url)
        print("queryied URL: " + url + " with status code " + str(r.status_code))
        if r.status_code == 200:
            self.json = r.json()
