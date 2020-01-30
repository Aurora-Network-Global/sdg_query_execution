class QueryFilters:
    """Filter element holding filter strings for affiliation, document type,
    people, time-ranges, funding and subject categories. Filters are applied either on an overall query level or within
    a single query definition. Filters and the corresponding filter definition are combined by the boolean operator AND.
    """

    @property
    def timerange(self):
        return self._timerange

    @property
    def query_filters(self):
        return self._query_filters

    def __init__(self,
                 timerange=None,
                 query_filters=None):
        self._timerange = timerange
        if query_filters is not None:
            self._query_filters = query_filters
        else:
            self._query_filters = []

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}

    def add_filter(self, query_filter):
        self._query_filters.append(query_filter)
