class Scival:

    def __init__(self, row):
        if row.__len__() > 36:
            if row[0] is not "-":
                self._title = row[0]
            else:
                self._title = None
            if row[1] is not "-":
                self._authors = row[1]
            else:
                self._authors = None
            if row[2] is not "-":
                self._number_of_authors = row[2]
            else:
                self._number_of_authors = None
            if row[3] is not "-":
                self._scopus_author_ids = row[3].split(', ')
            else:
                self._scopus_author_ids = []
            if row[4] is not "-":
                self._year = row[4]
            else:
                self._year = None
            if row[5] is not "-":
                self._scopus_source_title = row[5]
            else:
                self._scopus_source_title = None
            if row[6] is not "-":
                self._volume = row[6]
            else:
                self._volume = None
            if row[7] is not "-":
                self._issue = row[7]
            else:
                self._issue = None
            if row[8] is not "-":
                self._pages = row[8]
            else:
                self._pages = None
            if row[9] is not "-":
                self._issn = row[9]
            else:
                self._issn = None
            if row[10] is not "-":
                self._source_id = row[10]
            else:
                self._source_id = None
            if row[11] is not "-":
                self._source_type = row[11]
            else:
                self._source_type = None
            if row[12] is not "-":
                self._snip = row[12]
            else:
                self._snip = None
            if row[13] is not "-":
                self._cite_score = row[13]
            else:
                self._cite_score = None
            if row[14] is not "-":
                self._sjr = row[14]
            else:
                self._sjr = None
            if row[15] is not "-":
                self._field_weighted_view_impact = row[15]
            else:
                self._field_weighted_view_impact = None
            if row[16] is not "-":
                self._views = row[16]
            else:
                self._views = None
            if row[17] is not "-":
                self._citations = row[17]
            else:
                self._citations = None
            if row[18] is not "-":
                self._field_weighted_citation_impact = row[18]
            else:
                self._field_weighted_citation_impact = None
            if row[19] is not "-":
                self._output_in_top_percentiles = row[19]
            else:
                self._output_in_top_percentiles = None
            if row[20] is not "-":
                self._field_weighted_output_in_top_citation_percentiles = row[20]
            else:
                self._field_weighted_output_in_top_citation_percentiles = None
            if row[21] is not "-":
                self._reference = row[21]
            else:
                self._reference = None
            if row[22] is not "-":
                self._abstract_url = row[22]
            else:
                self._abstract_url = None
            if row[23] is not "-":
                self._doi = row[23]
            else:
                self._doi = None
            if row[24] is not "-":
                self._publication_type = row[24]
            else:
                self._publication_type = None
            if row[25] is not "-":
                self._eid = row[25]
            else:
                self._eid = None
            if row[26] is not "-":
                self._pubmed_id = row[26]
            else:
                self._pubmed_id = None
            if row[27] is not "-":
                self._institutions = row[27].split(', ')
            else:
                self._institutions = None
            if row[28] is not "-":
                self._scopus_affil_ids = row[28].split(', ')
            else:
                self._scopus_affil_ids = None
            if row[29] is not "-":
                self._scopus_affil_names = row[29].split('; ')
            else:
                self._scopus_affil_names = None
            if row[30] is not "-":
                self._country = row[30].split(', ')
            else:
                self._country = None
            if row[31] is not "-":
                self._all_science_classification_code = row[31].split('; ')
            else:
                self._all_science_classification_code = None
            if row[32] is not "-":
                self._all_science_classification_name = row[32].split('; ')
            else:
                self._all_science_classification_name = None
            if row[33] is not "-":
                self._topic_cluster_name = row[33]
            else:
                self._topic_cluster_name = None
            if row[34] is not "-":
                self._topic_cluster_number = row[34]
            else:
                self._topic_cluster_number = None
            if row[35] is not "-":
                self._topic_name = row[35]
            else:
                self.topic_name = None
            if row[36] is not "-":
                self.topic_number = row[36]
            else:
                self.topic_number = None
        else:
            self._title = None
            self._authors = None
            self._number_of_authors = None
            self._scopus_author_ids = None
            self._year = None
            self._scopus_source_title = None
            self._volume = None
            self._issue = None
            self._pages = None
            self._issn = None
            self._source_id = None
            self._source_type = None
            self._snip = None
            self._cite_score = None
            self._sjr = None
            self._field_weighted_view_impact = None
            self._views = None
            self._citations = None
            self._field_weighted_citation_impact = None
            self._output_in_top_percentiles = None
            self._field_weighted_output_in_top_citation_percentiles = None
            self._reference = None
            self._abstract_url = None
            self._doi = None
            self._publication_type = None
            self._eid = None
            self._pubmed_id = None
            self._institutions = []
            self._scopus_affil_ids = []
            self._scopus_affil_names = []
            self._country = []
            self._all_science_classification = []
            self._topic_cluster_name = None
            self._topic_cluster_number = None
            self._topic_name = None
            self.topic_number = None

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    @property
    def eid(self):
        return self._eid

    @property
    def title(self):
        return self._title
