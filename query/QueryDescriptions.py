class QueryDescriptions:
    """A query line holding an individual concept. A concept is a query string designed to retreive publications for
    a specific topic and is usually derived from single sentences, keywords or a short synopsis"""

    @property
    def query_description(self):
        return self._query_description

    def __init__(self, query_descriptions):
        if query_descriptions is not None:
            self._query_descriptions = query_descriptions
        else:
            self._query_descriptions = []

    def add_query_description(self, query_description):
        self._query_descriptions.append(query_description)

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}