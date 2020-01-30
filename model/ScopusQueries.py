class ScopusQueries:

    @property
    def search_strings(self):
        return self._search_strings

    @property
    def overall(self):
        return self._overall

    @overall.setter
    def overall(self, overall):
        self._overall = overall

    def __init__(self, search_strings=None, overall=""):
        if search_strings is not None:
            self._search_strings = search_strings
        else:
            self._search_strings = []
        self._overall = overall

    def add_search_string(self, search_string):
        self._search_strings.append(search_string)

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
