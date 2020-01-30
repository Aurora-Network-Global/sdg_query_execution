class QueryLine:
    """A query line holding an individual concept. A concept is a query string designed to retreive publications for
    a specific topic and is usually derived from single sentences, keywords or a short synopsis"""

    @property
    def field(self):
        return self._field

    @property
    def query_line(self):
        return self._query_line

    def __init__(self, field, query_line):
        self._field = field
        self._query_line = query_line

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
