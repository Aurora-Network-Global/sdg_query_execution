class Scival:

    def __init__(self, row):
        if row.__len__() > 36:
            if row['Title'] is not "-":
                self._title = row['Title']
            else:
                self._title = None
            if row['Authors'] is not "-":
                self._authors = row['Authors']
            else:
                self._authors = None
            if row['Number of Authors'] is not "-":
                self._number_of_authors = row['Number of Authors']
            else:
                self._number_of_authors = None
            if row['Scopus Author Ids'] is not "-":
                if row['Scopus Author Ids'] is not None:
                    self._scopus_author_ids = row['Scopus Author Ids'].split(', ')
            else:
                self._scopus_author_ids = []
            if row['Year'] is not "-":
                self._year = row['Year']
            else:
                self._year = None
            if row['Scopus Source title'] is not "-":
                self._scopus_source_title = row['Scopus Source title']
            else:
                self._scopus_source_title = None
            if row['Volume'] is not "-":
                self._volume = row['Volume']
            else:
                self._volume = None
            if row['Issue'] is not "-":
                self._issue = row['Issue']
            else:
                self._issue = None
            if row['Pages'] is not "-":
                self._pages = row['Pages']
            else:
                self._pages = None
            if row['ISSN'] is not "-":
                self._issn = row['ISSN']
            else:
                self._issn = None
            if row['Source ID'] is not "-":
                self._source_id = row['Source ID']
            else:
                self._source_id = None
            if row['Source-type'] is not "-":
                self._source_type = row['Source-type']
            else:
                self._source_type = None
            if row['SNIP 2017'] is not "-":
                self._snip = row['SNIP 2017']
            else:
                self._snip = None
            if row['CiteScore 2017'] is not "-":
                self._cite_score = row['CiteScore 2017']
            else:
                self._cite_score = None
            if row['SJR 2017'] is not "-":
                self._sjr = row['SJR 2017']
            else:
                self._sjr = None
            if row['Field-Weighted View Impact'] is not "-":
                self._field_weighted_view_impact = row['Field-Weighted View Impact']
            else:
                self._field_weighted_view_impact = None
            if row['Views'] is not "-":
                self._views = row['Views']
            else:
                self._views = None
            if row['Citations'] is not "-":
                self._citations = row['Citations']
            else:
                self._citations = None
            if row['Field-Weighted Citation Impact'] is not "-":
                self._field_weighted_citation_impact = row['Field-Weighted Citation Impact']
            else:
                self._field_weighted_citation_impact = None
            if row['Outputs in Top Citation Percentiles, per percentile'] is not "-":
                self._output_in_top_percentiles = row['Outputs in Top Citation Percentiles, per percentile']
            else:
                self._output_in_top_percentiles = None
            if row['Field-Weighted Outputs in Top Citation Percentiles, per percentile'] is not "-":
                self._field_weighted_output_in_top_citation_percentiles = row['Field-Weighted Outputs in Top Citation Percentiles, per percentile']
            else:
                self._field_weighted_output_in_top_citation_percentiles = None
            if row['Reference'] is not "-":
                self._reference = row['Reference']
            else:
                self._reference = None
            if row['Abstract'] is not "-":
                self._abstract_url = row['Abstract']
            else:
                self._abstract_url = None
            if row['DOI'] is not "-":
                self._doi = row['DOI']
            else:
                self._doi = None
            if row['Publication-type'] is not "-":
                self._publication_type = row['Publication-type']
            else:
                self._publication_type = None
            if row['EID'] is not "-":
                self._eid = row['EID']
            else:
                self._eid = None
            if row['PubMed ID'] is not "-":
                self._pubmed_id = row['PubMed ID']
            else:
                self._pubmed_id = None
            if row['Institutions'] is not "-":
                if row['Institutions'] is not None:
                    self._institutions = row['Institutions'].split(', ')
            else:
                self._institutions = None
            if row['Scopus affiliation IDs'] is not "-":
                if row['Scopus affiliation IDs'] is not None:
                    self._scopus_affil_ids = row['Scopus affiliation IDs'].split(', ')
            else:
                self._scopus_affil_ids = None
            if row['Scopus affiliation names'] is not "-":
                if row['Scopus affiliation names'] is not None:
                    self._scopus_affil_names = row['Scopus affiliation names'].split('; ')
            else:
                self._scopus_affil_names = None
            if row['Country'] is not "-":
                if row['Country'] is not None:
                    self._country = row['Country'].split(', ')
            else:
                self._country = None
            if row['All Science Journal Classification (ASJC) Code'] is not "-":
                if row['All Science Journal Classification (ASJC) Code'] is not None:
                    self._all_science_classification_code = row['All Science Journal Classification (ASJC) Code'].split('; ')
            else:
                self._all_science_classification_code = None
            if row['All Science Journal Classification (ASJC) Field Name'] is not "-":
                self._all_science_classification_name = row['All Science Journal Classification (ASJC) Field Name']
            else:
                self._all_science_classification_name = None
            if row['Topic Cluster name'] is not "-":
                self._topic_cluster_name = row['Topic Cluster name']
            else:
                self._topic_cluster_name = None
            if row['Topic Cluster number'] is not "-":
                self._topic_cluster_number = row['Topic Cluster number']
            else:
                self._topic_cluster_number = None
            if row['Topic name'] is not "-":
                self._topic_name = row['Topic name']
            else:
                self.topic_name = None
            if row['Topic number'] is not "-":
                self.topic_number = row['Topic number']
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
