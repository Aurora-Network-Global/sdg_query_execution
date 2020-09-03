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
        overall_filter_string = clean_up_line(get_filter_string(self._query.query_definitions.query_filters))
        overall_query_string = overall_filter_string
        query_length = len(overall_filter_string)
        for query_definition in self._query.query_definitions.query_definition:
            query_string = overall_filter_string
            for query_line in query_definition.query_lines:
                if query_line.query_line is not '':

                    # generate query term for indiviudal query line
                    query_term = query_line.field + '(' + clean_up_line(query_line.query_line) + ')'

                    # add query term to overall query string. if it is the first entry, connect by AND and open bracket,
                    # else add it by OR
                    if overall_query_string is overall_filter_string:
                        overall_query_string = '(' + query_term
                    else:
                        overall_query_string += ' OR ' + query_term

                    # add the query term to the query string. these are designed to be below the limit of 2800
                    # for the scopus api. If the addition of the query term would exceed this limit, the line is closed
                    # and added to the scopus search strings, otherwise it is added to the current search line.
                    if (query_length + len(query_term)) < 2800:
                        # add query term to query string. if it is the first entry, connect by AND and open bracket,
                        # else add it by OR
                        if query_string is overall_filter_string:
                            query_string += '(' + query_term
                        else:
                            query_string += ' OR ' + query_term
                    else:
                        scopus_queries.add_search_string(query_string + ')')
                        query_string = overall_filter_string + '(' + query_term
            if query_term is not '':
                scopus_queries.add_search_string(query_string + ')')
                query_string = overall_filter_string + '(' + query_term
        scopus_queries.add_search_string(query_string + ')')
        scopus_queries.overall = overall_query_string + ')'
        self._scopus_queries = scopus_queries
        return self._scopus_queries


def clean_up_line(line):
    new_line = re.sub(' +', ' ', line).replace('\n', '').replace('\t', '').replace('\u201c', '"')\
        .replace('\u201d', '"').replace('\u2018', '"').replace('\u2019', '"')
    return new_line


def get_filter_string(query_filters):
    string = ''
    if query_filters.timerange is not None:
        if query_filters.timerange.field is not '':
            string = '(' + query_filters.timerange.field + ' AFT ' + query_filters.timerange.start
            if query_filters.timerange.end is not '':
                string = string + ' AND ' + query_filters.timerange.field + ' BEF ' + query_filters.timerange.end
            string = string + ') AND '
    for query_filter in query_filters.query_filters:
        if query_filter.filter_type is 'subjectarea':
            string += '('
            for i, subjects in enumerate(query_filter.filter_term.split(' OR ')):
                if i > 0:
                    string += ' OR '
                string += ' LIMIT-TO(SUBJAREA, \'' + query_filter.filter_term + '\')'
            string += ') AND '
        elif query_filter.filter_type:
            string += '(' + query_filter.filter_field + '(' + query_filter.filter_term + ')) AND '
            string = string.replace(' OR ', ') OR ' + query_filter.filter_field + '(')
    return string
