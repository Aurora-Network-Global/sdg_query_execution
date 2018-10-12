import requests


class Unpaywall:

    def __init__(self, email):
        self.unpaywall_url = "https://api.unpaywall.org/my/request"
        self.email = email

    def get_data_by_doi(self, doi):
        url = self.unpaywall_url + '/' + doi + "?email=" + self.email
        r = requests.get(url)
        print("queryied URL: " + url + " with status code " + str(r.status_code))
        if r.status_code == 200:
            return r.json()
        else:
            return None
