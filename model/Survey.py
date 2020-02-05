class Survey:

    @property
    def survey_id(self):
        return self._survey_id

    @survey_id.setter
    def survey_id(self, survey_id):
        self._survey_id = survey_id

    @property
    def number_of_replies(self):
        return len(self._survey_results)

    @property
    def survey_results(self):
        return self._survey_results

    @survey_results.setter
    def survey_results(self, survey_results):
        self._survey_results = survey_results

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        self._project_id = project_id

    @property
    def cities(self):
        cities = []
        for result in self._survey_results:
            cities.append(result.city)
        return cities

    def __init__(self, survey_id, project_id, survey_results=None):
        self._survey_id = survey_id
        self._project_id = project_id
        if survey_results is None:
            self._survey_results = []
        else:
            self._survey_results = survey_results

    def __getstate__(self):
        state = self.__dict__.copy()
        return state
