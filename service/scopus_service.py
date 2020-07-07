from pybliometrics import scopus


def execute_query(scopus_queries):
    eids = []
    for search_string in scopus_queries.search_strings:
        search = scopus.ScopusSearch(search_string, refresh=True)
        print(search)
        eids = eids + search.get_eids()

    # convert to set in order to remove duplicates
    eids = set(eids)
    return eids