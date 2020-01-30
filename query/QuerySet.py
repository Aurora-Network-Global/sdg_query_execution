class QuerySet:
    """A container element to hold a list of query objects."""

    @property
    def queries(self):
        return self._queries

    def __init__(self, queries):
        if queries is not None:
            self._queries = queries
        else:
            self._queries = []

    def add_query(self, query):
        self._queries.append(query)

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}