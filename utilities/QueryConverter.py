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
        overall_filter_strings = get_filter_strings(self._query.query_definitions.query_filters)
        for query_definition in self._query.query_definitions.query_definition:
            queries = []
            for overall_filter_string in overall_filter_strings:
                overall_query_string = overall_filter_string
                query_length = len(overall_filter_string)
                query_string = overall_filter_string
                for query_line in query_definition.query_lines:
                    query_term = ''
                    if query_line.query_line is not '':

                        # generate query term for individual query line
                        query_term = query_line.field + '(' + clean_up_line(query_line.query_line) + ')'

                        # add query term to overall query string. if it is the first entry, connect by AND and open bracket,
                        # else add it by OR
                        if overall_query_string is overall_filter_string:
                            overall_query_string = ' AND (' + query_term
                        else:
                            overall_query_string += ' OR ' + query_term

                        # add the query term to the query string. these are designed to be below the limit of 2800
                        # for the scopus api. If the addition of the query term would exceed this limit, the line is closed
                        # and added to the scopus search strings, otherwise it is added to the current search line.
                        if (query_length + len(query_term)) < 2800:
                            # add query term to query string. if it is the first entry, connect by AND and open bracket,
                            # else add it by OR
                            if query_string is overall_filter_string:
                                query_string += ' AND (' + query_term
                            else:
                                query_string += ' OR ' + query_term
                        else:
                            queries.append(query_string + ')')
                            query_string = overall_filter_string + '(' + query_term
                    if query_string is not '':
                        queries.append(query_string + ')')
                        query_string = overall_filter_string + '(' + query_term

            scopus_queries.add_search_string(queries)
            scopus_queries.add_search_id(str(self._query.identifier) + '.' + str(query_definition.identifier))
        self._scopus_queries = scopus_queries
        return self._scopus_queries


def clean_up_line(line):
    new_line = re.sub(' +', ' ', line).replace('\n', '').replace('\t', '').replace('\u201c', '"') \
        .replace('\u201d', '"').replace('\u2018', '"').replace('\u2019', '"').strip()
    return new_line


def get_filter_strings(query_filters):
    list_of_filter_lists = []
    timerange_filter = get_timerange_filter_string(query_filters.timerange)
    if timerange_filter != '':
        list_of_filter_lists.append([timerange_filter])
    for query_filter in query_filters.query_filters:
        if query_filter.filter_type == 'subjectarea':
            subjectearea_filter = get_subjectarea_filter(query_filter)
            if subjectearea_filter != '':
                list_of_filter_lists.append([subjectearea_filter])
        else:
            list_of_filter_lists.append(get_filter_list(query_filter))
    return get_filter_lists(list_of_filter_lists)


def get_timerange_filter_string(timerange):
    string = ''
    if timerange is not None:
        if timerange.field is not '':
            string = '(' + timerange.field + ' AFT ' + timerange.start
            if timerange.end is not '':
                string = string + ' AND ' + timerange.field + ' BEF ' + timerange.end
            string = string + ')'
    return clean_up_line(string)


def get_subjectarea_filter(query_filter):
    string = '('
    for i, subjects in enumerate(query_filter.filter_term.split(' OR ')):
        if i > 0:
            string += ' OR '
        string += ' LIMIT-TO(SUBJAREA, \'' + query_filter.filter_term + '\')'
    string += ')'
    return clean_up_line(string)


def get_filter_list(query_filter):
    filter_list = []
    for filter_term in query_filter.filter_term.split('|'):
        string = '({}({}))'.format(query_filter.filter_field, filter_term)
        string = clean_up_line(string.replace(' OR ', ') OR ' + query_filter.filter_field + '('))
        filter_list.append(string)
    return filter_list


def get_filter_lists(list_of_filter_lists):
    list = []
    for filter_list in list_of_filter_lists:
        if len(list) == 0:
            list = filter_list
        else:
            list = [' and '.join((i, j)) for i in list for j in filter_list]
    return list
