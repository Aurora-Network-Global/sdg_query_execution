class QueryDefinition:
    """A query definition holds a larger subset of an extended query. Each query consists at least of one query
    line, defining a particular concept. Multiple concepts within the query are represented by individual query lines,
    which are combined by the boolean operator OR."""

    @property
    def query_lines(self):
        return self._query_lines

    @property
    def identifier(self):
        return self._identifier

    @property
    def descriptions(self):
        return self._descriptions

    @property
    def query_filters(self):
        return self._query_filters

    @query_filters.setter
    def query_filters(self, query_filters):
        self._query_filters = query_filters

    def __init__(self, identifier,
                 query_lines=None,
                 query_filters=None,
                 descriptions=None,
                 ):
        if query_lines is not None:
            self._query_lines = query_lines
        else:
            self._query_lines = []
        if query_filters is not None:
            self._query_filters = query_filters
        else:
            self._query_filters = []
        if descriptions is not None:
            self._descriptions = descriptions
        else:
            self._descriptions = []
        self._identifier = identifier

    def add_query_line(self, query_line):
        self.query_lines.append(query_line)

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
