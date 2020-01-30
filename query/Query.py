from datetime import date


class Query:
    """The main definition object of a query. Contains information about the creator, contributors, the query
    definitions and the applied filters."""

    @property
    def identifier(self):
        return self._identifier

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def creator(self):
        return self._creator

    @property
    def contributor(self):
        return self._contributor

    @property
    def date_modified(self):
        return self._date_modified

    @property
    def query_definitions(self):
        return self._query_definitions

    @property
    def licence(self):
        return self._licence

    @property
    def licence_href(self):
        return self._licence_href

    @query_definitions.setter
    def query_definitions(self, query_definitions):
        self._query_definitions = query_definitions

    def __init__(self,
                 creator='',
                 identifier='',
                 query_definitions=None,
                 title='',
                 description='',

                 contributor='',
                 licence='CC-BY v4 INT',
                 licence_href='http://creativecommons.org/licenses/by/4.0/',
                 date_modified=str(date.today())
                 ):
        self._creator = creator
        self._contributor = contributor

        if query_definitions is not None:
            self._query_definitions = query_definitions
        else:
            self._query_definitions = None
        self._title = title
        self._identifier = identifier
        self._description = description
        self._date_modified = str(date.today())
        self._licence = licence
        self._licence_href = licence_href
        self._date_modified = date_modified

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
