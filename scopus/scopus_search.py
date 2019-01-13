import os
import sys
import xml.etree.ElementTree as ET

from scopus.utils import download, ns
from scopus.scopus_api import ScopusAbstract

SCOPUS_SEARCH_DIR = os.path.expanduser('~/.scopus/search')

if not os.path.exists(SCOPUS_SEARCH_DIR):
    os.makedirs(SCOPUS_SEARCH_DIR)


class ScopusSearch(object):
    @property
    def EIDS(self):
        """List of EIDs retrieved."""
        return self._EIDS

    def __init__(self, query, fields='eid', count=100, start=0, refresh=False, query_id='1'):
        """Class to search a query, and retrieve a list of EIDs as results.

        Parameters
        ----------
        query : str
            A string of the query.

        fields : str (optional, default='eid')
            The fields you want returned.  Allowed fields are specified in
            https://dev.elsevier.com/guides/ScopusSearchViews.htm.  Since
            currently only EIDs are stored, this parameter is being kept
            for later use only.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        start : int (optional, default=0)
            The entry number of the first search item to start with.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        Raises
        ------
        Exception
            If the number of search results exceeds max_entries.

        Notes
        -----
        XML results are cached in ~/.scopus/search/{query}.

        The EIDs are stored as a property named EIDS.
        """

        self.query = query
        qfile = os.path.join(SCOPUS_SEARCH_DIR,
                             # We need to remove / in a DOI here so we can save
                             # it as a file.
                             query_id)

        if os.path.exists(qfile) and not refresh:
            with open(qfile) as f:
                self._EIDS = [eid for eid in
                              f.read().strip().split('\n')
                              if eid]
        else:
            # No cached file exists, or we are refreshing.
            # First, we get a count of how many things to retrieve
            url = 'https://api.elsevier.com/content/search/scopus'
            params = {'query': query, 'field': fields, 'count': count, 'cursor': '*'}
            response = download(url=url, params=params, accept="json")
            results = response.json()

            N = results['search-results']['opensearch:totalResults']
            print(N + ' results in Scopus found')
            try:
                N = int(N)
            except:
                N = 0
            self._EIDS = []
            print(str(N))
            cursor = '*'
            while N > 0:
                print(cursor)
                params = {'query': query, 'fields': fields,
                          'count': count, 'cursor': cursor}
                try:
                    resp = download(url=url, params=params, accept="json")
                except:
                    break

                results = resp.json()
                if 'entry' in results.get('search-results', []):
                    self._EIDS += [str(r['eid']) for
                                   r in results['search-results']['entry']]
                N -= count
                cursor = results['search-results']['cursor']['@next']
            with open(qfile, 'wb') as f:
                for eid in self.EIDS:
                    f.write('{}\n'.format(eid).encode('utf-8'))

    def __str__(self):
        s = """{query}
        Resulted in {N} hits.
    {entries}"""
        return s.format(query=self.query,
                        N=len(self.EIDS),
                        entries='\n    '.join(self.EIDS))

    @property
    def org_summary(self):
        """Summary of search results."""
        s = ''
        for i, eid in enumerate(self.EIDS):
            abstract = ScopusAbstract(eid)
            if abstract.aggregationType == 'Journal':
                s += '{0}. {1}\n'.format(i + 1, abstract)
        return s
