class AllResponses:

    def __init__(self, identifier, query_title, project_id):
        self.id = identifier
        self.scopus_abstract_retrieval = None
        self.unpaywall_response = None
        self.altmetric_response = None
        self.scival_data = None
        self.query_title = query_title
        self.project_id = project_id
        self.accepted = None

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['id']
        return state
