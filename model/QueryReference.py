class QueryReference:

    @property
    def query_id(self):
        return self.query_id

    @property
    def query_description(self):
        return self._query_description

    @property
    def query_name(self):
        return self._query_name

    @query_id.setter
    def query_id(self, query_id):
        self._query_id = query_id

    @query_name.setter
    def query_name(self, query_name):
        self._query_name = query_name

    @query_description.setter
    def query_description(self, query_description):
        self._query_description = query_description

    def __init__(self, query_id, query_description, query_name):
        self._query_id = query_id
        self._query_description = query_description
        self._query_name = query_name

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
