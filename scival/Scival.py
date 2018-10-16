class Scival:

    def __init__(self, row):
        if row.__len__() == 32:
            self._title = row[0]
            self._authors = row[1]
            self._number_of_authors = row[2]
            self._scopus_author_ids = row[3].split(', ')
            self._year = row[4]
            self._scopus_source_title = row[5]
            self._volume = row[6]
            self._issue = row[7]
            self._pages = row[8]
            self._issn = row[9]
            self._source_id = row[10]
            self._source_type = row[11]
            self._snip = row[12]
            self._cite_score = row[13]
            self._sjr = row[14]
            self._field_weighted_view_impact = row[15]
            self._views = row[16]
            self._citations = row[17]
            self._field_weighted_citation_impact = row[18]
            self._output_in_top_percentiles = row[19]
            self._field_weighted_output_in_top_citation_percentiles = row[20]
            self._reference = row[21]
            self._abstract_url = row[22]
            self._doi = row[23]
            self._publication_type = row[24]
            self._eid = row[25]
            self._pubmed_id = row[26]
            self._institutions = row[27].split(', ')
            self._scopus_affil_ids = row[28].split(', ')
            self._scopus_affil_names = row[29].split('; ')
            self._country = row[30].split(', ')
            self._all_science_classification = row[31].split('; ')
        else:
            self._title = ''
            self._authors = ''
            self._number_of_authors = 0
            self._scopus_author_ids = []
            self._year = 0
            self._scopus_source_title = ''
            self._volume = ''
            self._issue = ''
            self._pages = ''
            self._issn = ''
            self._source_id = ''
            self._source_type = ''
            self._snip = 1
            self._cite_score = 1
            self._sjr = 1
            self._field_weighted_view_impact = 1
            self._views = 0
            self._citations = 0
            self._field_weighted_citation_impact = 1
            self._output_in_top_percentiles = 100
            self._field_weighted_output_in_top_citation_percentiles = 100
            self._reference = ''
            self._abstract_url = ''
            self._doi = ''
            self._publication_type = ''
            self._eid = ''
            self._pubmed_id = ''
            self._institutions = []
            self._scopus_affil_ids = []
            self._scopus_affil_names = []
            self._country = []
            self._all_science_classification = []

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    @property
    def eid(self):
        return self._eid

    @property
    def title(self):
        return self._title
