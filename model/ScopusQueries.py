class ScopusQueries:

    @property
    def search_strings(self):
        return self._search_strings

    @property
    def search_ids(self):
        return self._search_ids

    @search_ids.setter
    def search_ids(self, search_id):
        self._search_ids = search_id

    @property
    def overall(self):
        return self._overall

    @overall.setter
    def overall(self, overall):
        self._overall = overall

    def __init__(self, search_strings=None, overall="", search_ids=None):
        if search_strings is not None:
            self._search_strings = search_strings
        else:
            self._search_strings = []
        self._overall = overall
        if search_ids is None:
            self._search_ids = []
        else:
            self._search_ids = search_ids

    def add_search_string(self, search_string):
        self._search_strings.append(search_string)

    def add_search_id(self, search_id):
        if search_id is None:
            self._search_ids.append(str(len(self._search_ids)))
        elif search_id == '':
            self._search_ids.append(str(len(self._search_ids)))
        else:
            self._search_ids.append(search_id)

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
