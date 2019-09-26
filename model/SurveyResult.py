class SurveyResult:

    def __init__(self, row):
        self._session = row[9]
        self._judgements = []
        for i in range(25, 124):
            self._judgements.append({'eid': row[100 + i], 'judgement': ('Yes' in row[i])})
        self._unselected_keywords = []
        self._selected_keywords = []
        for i in range(227, 326):
            if row[i] is '':
                self._unselected_keywords.append(i - 226)
            else:
                self._selected_keywords.append(i - 226)
        self._suggested_keywords = row[328]
        self._suggested_journals = row[435]
        self._unselected_journals = []
        self._selected_journals = []
        for i in range(334, 433):
            if row[i] is '':
                self._unselected_journals.append(i - 333)
            else:
                self._selected_journals.append(i - 333)

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def get_selected_papers(self):
        selected = []
        for paper in self._judgements:
            if paper['judgement']:
                selected.append(paper['eid'])
        return selected

    def get_unselected_papers(self):
        unselected = []
        for paper in self._judgements:
            if not paper['judgement']:
                unselected.append(paper['eid'])
        return unselected

    def replace_keywords(self, keywords):
        for i in range(0, self._selected_keywords.__len__()-1):
            index = int(self._unselected_keywords[i])
            self._selected_keywords[i] = keywords[index]
        for i in range(0, self._unselected_keywords.__len__()-1):
            index = int(self._unselected_keywords[i])
            self._unselected_keywords[i] = keywords[index]

    def replace_journals(self, journals):
        for i in range(0, self._selected_journals.__len__()-1):
            index = int(self._unselected_journals[i])
            self._selected_journals[i] = journals[index]
        for i in range(0, self._unselected_journals.__len__() - 1):
            index = int(self._unselected_journals[i])
            self._unselected_journals[i] = journals[index]


