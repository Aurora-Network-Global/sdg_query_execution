class AllResponses:

    def __init__(self, identifier):
        self.id = identifier
        self.scopus_abtract_retrieval = None
        self.unpaywall_response = None
        self.altmetric_response = None
        self.scival_data = None

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['id']
        return state
