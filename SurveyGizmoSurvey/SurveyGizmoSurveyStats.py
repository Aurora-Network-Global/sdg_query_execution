import requests
from flask import current_app as app
from utilities.utils import wordlist_to_freq_dict


class SurveyGizmoSurveyStats:

    @property
    def cities_frequencies(self):
        return self._cities_frequencies

    def number_replies(self):
        return self._number_replies

    def __init__(self, survey_id):
        with app.app_context():
            self._key = app.config.get("SURVEY_GIZMO_API_KEY")
            self._secret = app.config.get("SURVEY_GIZMO_API_SECRET")
            self._survey_gizmo_url = app.config.get("SURVEY_GIZMO_URL")
        self._number_replies = 0
        self._base_url = self._survey_gizmo_url + '/survey/' + survey_id
        url = self._base_url + '/surveyresponse' + '?api_token=' + self._key + '&api_token_secret=' + self._secret + '&filter[value][0]=Complete&filter[field][0]=status&filter[operator][0]==&filter[field][1]=is_test_data&filter[operator][1]==&filter[value][1]=0'
        r = requests.get(url)
        cities = []
        if r.status_code == 200:
            data = r.json()['data']
            self._number_replies = data.__len__()
            for datum in data:
                cities.append(datum['city'])
        self._cities_frequencies = wordlist_to_freq_dict(cities)



