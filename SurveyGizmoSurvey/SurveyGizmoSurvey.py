import requests
from flask import current_app as app

from model import SurveyResult

class SurveyGizmoSurvey:
    def __init__(self, survey_id):
        with app.app_context():
            self._key = app.config.get("SURVEY_GIZMO_API_KEY")
            self._secret = app.config.get("SURVEY_GIZMO_API_SECRET")
            self._survey_gizmo_url = app.config.get("SURVEY_GIZMO_URL")

        self._base_url = self._survey_gizmo_url + '/survey/' + survey_id
        url = self._base_url + '?api_token=' + self._key + '&api_token_secret=' + self._secret
        print('requesting url: ' + url)
        r = requests.get(url)
        print(r.status_code)
        if r.status_code == 200:
            pages = r.json()['data']['pages']
            for page in pages:
                title = page['title']['English'].lower()
                if 'publications contributing to this sdg' in title:
                    for question in page['questions']:
                        if 'MATRIX' in question['type']:
                            self._matrix_question_number = question['id']
                elif 'select keywords' in title:
                    for question in page['questions']:
                        if 'CHECKBOX' in question['type']:
                            self._keywords_question_number = question['id']
                            self._keywords_options_number = []
                            for option in question['options']:
                                self._keywords_options_number.append(option['id'])
                        elif 'ESSAY' in question['type']:
                            self._keyword_suggestion_number = question['id']
                elif 'select the journals' in title:
                    for question in page['questions']:
                        if 'CHECKBOX' in question['type']:
                            self._journal_question_number = question['id']
                            self._journal_options_number = []
                            for option in question['options']:
                                self._journal_options_number.append(option['id'])
                        elif 'ESSAY' in question['type']:
                            self._journal_suggestion_number = question['id']
                else:
                    continue

    def get_survey_results(self):
        url = self._base_url + '/surveyresponse' + '?api_token=' + self._key + '&api_token_secret=' + self._secret + '&filter[value][0]=Complete&filter[field][0]=status&filter[operator][0]==&filter[field][1]=is_test_data&filter[operator][1]==&filter[value][1]=0'
        print('getting singel result from ' + url)
        r = requests.get(url)
        survey_results = []
        print(r.status_code)
        if r.status_code == 200:
            print(r.json()['data'].__len__())
            for datum in r.json()['data']:
                result = datum['survey_data']
                single_result = SurveyResult.SurveyResult()
                single_result._session = datum['session_id']
                try:
                    single_result._suggested_keywords = result[str(self._keyword_suggestion_number)]['answer'].split('\n')
                except:
                    print('no keyword suggestions given.')
                try:
                    single_result._suggested_journals = result[str(self._journal_suggestion_number)]['answer'].split('\n')
                except:
                    print('no journal suggestions given')
                try:
                    for selected_journal_option in result[str(self._journal_question_number)]['options']:
                        single_result._selected_journals.append(result[str(self._journal_question_number)]['options'][str(selected_journal_option)]['answer'])
                except:
                    print('no journals selected')
                try:
                    for selected_keyword_option in result[str(self._keywords_question_number)]['options']:
                        single_result._selected_keywords.append(result[str(self._keywords_question_number)]['options'][str(selected_keyword_option)]['answer'])
                except:
                    print('no keywords selected')

                matrix_answers = result[str(self._matrix_question_number)]['subquestions']
                for i in range(1, 100):
                    if i not in single_result._selected_journals:
                        single_result._unselected_journals.append(i)
                    if i not in single_result._selected_keywords:
                        single_result._unselected_keywords.append(i)
                    try:
                        eid = result[str(self._matrix_question_number)]['subquestions'][list(matrix_answers)[i+100]]['answer']
                        judgement = result[str(self._matrix_question_number)]['subquestions'][list(matrix_answers)[i]]['answer']
                        single_result._judgements.append({'eid': eid, 'judgement': ('Yes' in judgement)})
                    except:
                        print('no data available for ' + str(i))
                survey_results.append(single_result)
        return survey_results


