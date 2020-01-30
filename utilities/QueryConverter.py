import re

from model.ScopusQueries import ScopusQueries


class QueryConverter:

    @property
    def query(self):
        return self._query

    @property
    def scopus_queries(self):
        if self._query is not None:
            self.calculate_scopus_queries()
        return self._scopus_queries

    @property
    def mycore_queries(self):
        return self._mycore_queries

    def __init__(self, query):
        self._query = query
        self._scopus_queries = ScopusQueries
        self._mycore_queries = None

    def calculate_scopus_queries(self):
        scopus_queries = ScopusQueries()
        overall_filter_string = get_filter_string(self._query.query_definitions.query_filters)
        query_string = overall_filter_string
        overall_query_string = overall_filter_string
        query_length = query_string.__len__()
        for query_definition in self._query.query_definitions.query_definition:
            for query_line in query_definition.query_lines:
                if query_line.query_line is not "":
                    query_line_string = query_line.field + '(' + re.sub(' +', ' ', query_line.query_line.replace('\n', '')) + ')'
                    overall_query_string = query_line.field + '(' + re.sub(' +', ' ', query_line.query_line.replace('\n', '')) + ')'
                    if (query_length + query_line_string.__len__()) < 2800:
                        if query_string is overall_filter_string:
                            if query_string is not '':
                                query_string = query_string + ' AND ('
                                overall_query_string = overall_query_string + ' AND ('
                            else:
                                query_string = query_string + '('
                                overall_query_string = overall_query_string + '('
                        else:
                            query_string = query_string + ' OR '
                            overall_query_string = overall_query_string + ' OR '
                        query_string = query_string + query_line_string
                    else:
                        overall_query_string = overall_query_string + ' AND ('
                        scopus_queries.add_search_string(query_string + ')')
                        query_string = overall_filter_string + ' AND (' + query_line_string
        scopus_queries.add_search_string(query_string + ')')
        scopus_queries.overall = overall_query_string + ')'
        self._scopus_queries = scopus_queries
        return self._scopus_queries


def get_filter_string(query_filters):
    string = ''
    if query_filters.timerange is not None:
        if query_filters.timerange.field is not '':
            string = '(' + query_filters.timerange.field + ' AFT ' + query_filters.timerange.start
            if query_filters.timerange.end is not '':
                string = string + ' AND ' + query_filters.timerange.field + ' BEF ' + query_filters.timerange.end
            string = string + ')'
    for query_filter in query_filters.query_filters:
        if string != "":
            string += " AND "
        if query_filter.filter_type is 'subjectarea':
            string += "("
            for i, subjects in enumerate(query_filter.filter_term.split(" OR ")):
                if i > 0:
                    string += " OR "
                string += " LIMIT-TO(SUBJAREA, \"" + query_filter.filter_term + "\")"
            string += ")"
        else:
            string += "("
            string += query_filter.filter_field + "(" + query_filter.filter_term + ")"
    return string
