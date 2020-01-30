from query.QueryFilters import QueryFilters


class QueryDefintions:
    """A query definition holds a subset of the query. Each query can consist of a number of query
    definitions, which in turn hold several query lines for individual concepts. Filters defined in this class apply to
    the overall query and cen be extended by individual filters within each query definition."""

    @property
    def query_definition(self):
        return self._query_definition

    @query_definition.setter
    def query_definition(self, query_definition):
        self._query_definition = query_definition

    @property
    def query_filters(self):
        return self._query_filters

    @query_filters.setter
    def query_filters(self, query_filters):
        self._query_filters = query_filters

    @property
    def syntax(self):
        return self._syntax

    @syntax.setter
    def syntax(self, syntax):
        self._syntax = syntax

    def __init__(self, query_definition=None, query_filters=None, syntax="SCOPUS"):
        if query_definition is not None:
            self._query_definition = query_definition
        else:
            self._query_definition = []
        if query_filters is not None:
            self._query_filters = query_filters
        else:
            self._query_filters = QueryFilters()
        self._syntax = syntax

    def add_query_definition(self, query_defintion):
        self._query_definition.append(query_defintion)


    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
