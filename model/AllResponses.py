class AllResponses:

    def __init__(self, identifier, query_title, query_id):
        self.id = identifier
        self.scopus_abtract_retrieval = None
        self.unpaywall_response = None
        self.altmetric_response = None
        self.scival_data = None
        self.query_title = query_title
        self.query_id = query_id

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['id']
        return state
