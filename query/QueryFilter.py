class QueryFilter:
    """Filter element holding filter strings for affiliation, document type,
    people, time-ranges, funding and subject categories. Filters are applied either on an overall query level or within
    a single query definition. All filters and the corresponding filter definitions are combined by the boolean operator
     AND.
    """

    @property
    def filter_field(self):
        return self._filter_field

    @property
    def filter_type(self):
        return self._filter_type

    @property
    def filter_term(self):
        return self._filter_term

    @filter_field.setter
    def filter_field(self, filter_field):
        self._filter_field = filter_field

    @filter_type.setter
    def filter_type(self, filter_type):
        self._filter_type = filter_type

    @filter_term.setter
    def filter_term(self, filter_term):
        self._filter_term = filter_term

    def __init__(self,
                 filter_field="",
                 filter_type="",
                 filter_term=""):
        self._filter_field = filter_field
        self._filter_type = filter_type
        self._filter_term = filter_term

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
