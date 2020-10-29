class AllResponses:

    def __init__(self, identifier, query_title, project_id, query_id=''):
        self.id = identifier
        self.scopus_abstract_retrieval = None
        self.unpaywall_response = None
        self.altmetric_response = None
        self.scival_data = None
        self.query_title = query_title
        self.project_id = project_id
        self.query_id = query_id
        self.accepted = None

    def add_query_id(self, query_id):
        if self.query_id == '':
            self.query_id = query_id
        else:
            self.query_id = self.query_id + '; ' + query_id

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['id']
        return state
