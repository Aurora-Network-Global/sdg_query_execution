import requests
from flask import current_app as app

from model.Survey import Survey
from model.SurveyResult import SurveyResult


class SurveyGizmo:
    """
    A class that retrieves survey data from a Survey Gizmo survey
    """

    @property
    def survey(self):
        """
        the survey object as obtained from Survey Gizmo
        :return: the survey object
        """
        return self._survey

    def __init__(self, survey_id, project_id):
        # get the credentials from the config
        with app.app_context():
            self._key = app.config.get("SURVEY_GIZMO_API_KEY")
            self._secret = app.config.get("SURVEY_GIZMO_API_SECRET")

        # the urls to retrieve the structure of the survey and the data
        survey_structure_url = 'https://restapi.surveygizmo.eu/v5/survey/{}?api_token={}&api_token_secret={}'
        survey_data_url = 'https://restapi.surveygizmo.eu/v5/survey/{}/surveyresponse?api_token={}&api_token_secret={}&filter[value][0]=Complete&filter[field][0]=status&filter[operator][0]==&filter[field][1]=is_test_data&filter[field][1]==&filter[field][1]=0'

        r = requests.get(survey_structure_url.format(survey_id, self._key, self._secret))
        if r.status_code == 200:
            print('collected survey structure')
            self._survey_structure = r.json()
            pages = self._survey_structure['data']['pages']
            for page in pages:
                title = page['title']['English'].lower()
                if 'publications contributing to this sdg' in title:
                    for question in page['questions']:
                        if 'MATRIX' in question['type']:
                            self._matrix_question_number = question['id']
                            print('contributing publications question found : {}'.format(self._matrix_question_number))
                elif 'select keywords' in title:
                    for question in page['questions']:
                        if 'CHECKBOX' in question['type']:
                            self._keywords_question_number = question['id']
                            print('keywords question found : {}'.format(self._keywords_question_number))
                            self._keywords_options_number = []
                            for option in question['options']:
                                self._keywords_options_number.append(option['id'])
                        elif 'ESSAY' in question['type']:
                            self._keyword_suggestion_number = question['id']
                            print('keywords suggestion found : {}'.format(self._keyword_suggestion_number))
                elif 'select the journals' in title:
                    for question in page['questions']:
                        if 'CHECKBOX' in question['type']:
                            self._journal_question_number = question['id']
                            print('journal question found : {}'.format(self._journal_question_number))
                            self._journal_options_number = []
                            for option in question['options']:
                                self._journal_options_number.append(option['id'])
                        elif 'ESSAY' in question['type']:
                            self._journal_suggestion_number = question['id']
                            print('journal suggestion found : {}'.format(self._journal_suggestion_number))
                elif 'glossary with terms' in title:
                    for question in page['questions']:
                        if 'MULTI_TEXTBOX' in question['type']:
                            self._glossary_question_number = question['id']
                            print('glossaries suggestion found : {}'.format(self._glossary_question_number))
                else:
                    continue
            r = requests.get(survey_data_url.format(survey_id, self._key, self._secret))
            survey_results = []
            if r.status_code == 200:
                self._survey_data = r.json()
                print('collecting survey data')
                data = r.json()['data']
                for datum in data:
                    city = datum['city']
                    result = datum['survey_data']
                    country = datum['country']
                    latitude = datum['latitude']
                    longitude = datum['longitude']
                    session = datum['session_id']
                    try:
                        suggested_keywords = result[str(self._keyword_suggestion_number)]['answer'].split('\n')\
                            .replace('\r', '')
                    except KeyError:
                        suggested_keywords = []

                    try:
                        suggested_journals = result[str(self._journal_suggestion_number)]['answer'].split('\n')\
                        .replace('\r', '')
                    except KeyError:
                        suggested_journals = []

                    selected_journals = []
                    try:
                        for selected_journal_option in result[str(self._journal_question_number)]['options']:
                            selected_journals.append(
                                int(result[str(self._journal_question_number)]['options'][str(selected_journal_option)][
                                    'answer']))
                    except KeyError:
                        selected_journals = []

                    selected_keywords = []
                    try:
                        for selected_keyword_option in result[str(self._keywords_question_number)]['options']:
                            selected_keywords.append(
                                int(result[str(self._keywords_question_number)]['options'][str(selected_keyword_option)][
                                    'answer']))
                    except KeyError:
                        print('no keywords selected')

                    glossaries = []
                    try:
                        for suggestion in result[str(self._glossary_question_number)]['options']:
                            glossaries.append(suggestion['answer'])
                    except:
                        print('no keywords selected')

                    try:
                        matrix_answers = result[str(self._matrix_question_number)]['subquestions']
                    except KeyError:
                        print('no matrix questions asked')

                    unselected_journals = []
                    unselected_keywords = []
                    judgements = []
                    for i in range(1, 100):
                        if i not in selected_journals:
                            unselected_journals.append(i)
                        if i not in selected_keywords:
                            unselected_keywords.append(i)
                        try:
                            eid = result[str(self._matrix_question_number)]['subquestions'][list(matrix_answers)[i + 100]][
                                'answer']
                            judgement = result[str(self._matrix_question_number)]['subquestions'][list(matrix_answers)[i]][
                                'answer']
                            judgements.append({'eid': eid, 'judgement': ('Yes' in judgement)})
                        except KeyError:
                            pass
                    survey_results.append(SurveyResult(selected_journals=selected_journals,
                                                       unselected_journals=unselected_journals,
                                                       selected_keywords=selected_keywords,
                                                       unselected_keywords=unselected_keywords,
                                                       suggested_keywords=suggested_keywords,
                                                       suggested_journals=suggested_journals,
                                                       judgements=judgements,
                                                       session=session,
                                                       city=city,
                                                       suggested_glossaries=glossaries))
            self._survey = Survey(survey_id=survey_id,
                                  project_id=project_id,
                                  survey_results=survey_results)
