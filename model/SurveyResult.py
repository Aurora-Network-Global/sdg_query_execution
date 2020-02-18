class SurveyResult:

    @property
    def selected_journals(self):
        return self._selected_journals

    @selected_journals.setter
    def selected_journals(self, selected_journals):
        self._selected_journals = selected_journals

    @property
    def unselected_journals(self):
        return self._unselected_journals

    @unselected_journals.setter
    def unselected_journals(self, unselected_journals):
        self._unselected_journals = unselected_journals

    @property
    def suggested_journals(self):
        return self._suggested_journals

    @suggested_journals.setter
    def suggested_journals(self, suggested_journals):
        self._suggested_journals = suggested_journals

    @property
    def selected_keywords(self):
        return self._selected_keywords

    @selected_keywords.setter
    def selected_keywords(self, selected_keywords):
        self._selected_keywords = selected_keywords

    @property
    def unselected_keywords(self):
        return self._unselected_keywords

    @unselected_keywords.setter
    def unselected_keywords(self, unselected_keywords):
        self._unselected_keywords = unselected_keywords

    @property
    def suggested_keywords(self):
        return self._suggested_keywords

    @suggested_keywords.setter
    def suggested_keywords(self, suggested_keywords):
        self._suggested_keywords = suggested_keywords

    @property
    def suggested_glossaries(self):
        return self._suggested_glossaries

    @suggested_glossaries.setter
    def suggested_glossaries(self, suggested_glossaries):
        self._suggested_glossaries = suggested_glossaries

    @property
    def judgements(self):
        return self._judgements

    @judgements.setter
    def judgements(self, judgements):
        self._judgements = judgements

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    def __init__(self, selected_journals=None,
                 unselected_journals=None,
                 selected_keywords=None,
                 unselected_keywords=None,
                 judgements=None,
                 suggested_keywords=None,
                 suggested_glossaries=None,
                 suggested_journals=None,
                 session='',
                 city='',
                 country='',
                 longitude='',
                 latitude='',
                 terminology_addition=None):
        if unselected_journals is None:
            self._unselected_journals = []
        else:
            self._unselected_journals = unselected_journals
        if selected_journals is None:
            self._selected_journals = []
        else:
            self._selected_journals = selected_journals
        if unselected_keywords is None:
            self._unselected_keywords = []
        else:
            self._unselected_keywords = unselected_keywords
        if selected_keywords is None:
            self._selected_keywords = []
        else:
            self._selected_keywords = selected_keywords
        if suggested_keywords is None:
            self._suggested_keywords = []
        else:
            self._suggested_keywords = suggested_keywords
        if suggested_journals is None:
            self._suggested_journals = []
        else:
            self._suggested_journals = suggested_journals
        if suggested_glossaries is None:
            self._suggested_glossaries = []
        else:
            self._suggested_glossaries = suggested_glossaries
        if judgements is None:
            self._judgements = []
        else:
            self._judgements = judgements
        if terminology_addition is None:
            self._terminology_addition = []
        else:
            self._terminology_addition = terminology_addition
        self._session = session
        self._city = city

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def get_paper_selection(self):
        selected = []
        unselected = []
        for paper in self._judgements:
            if paper['judgement']:
                selected.append(paper['eid'])
            else:
                unselected.append(paper['eid'])
        return selected, unselected
