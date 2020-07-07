class Project:

    @property
    def project_id(self):
        return self._project_id

    @property
    def name(self):
        return self._name

    @property
    def isQueryDefined(self):
        return self._isQueryDefined

    @property
    def isEidsCollecting(self):
        return self._isEidsCollecting

    @property
    def isEidsCollected(self):
        return self._isEidsCollected

    @property
    def isDataCollected(self):
        return self._isDataCollected

    @property
    def isDataCollecting(self):
        return self._isDataCollecting

    @property
    def isTestdata(self):
        return self._isTestdata

    @property
    def isScivalData(self):
        return self._isScivalData

    @property
    def isEidslist(self):
        return self._isEidslist

    @property
    def isQueryRun(self):
        return self._isQueryRun

    @property
    def isIndexPresent(self):
        return self._isIndexPresent

    @property
    def isReferencesCollecting(self):
        return self._isReferencesCollecting

    @property
    def isReferencesCollected(self):
        return self._isReferencesCollected

    @property
    def queries(self):
        return self._queries

    @name.setter
    def name(self, name):
        self._name = name

    @isQueryDefined.setter
    def isQueryDefined(self, isQueryDefined):
        self._isQueryDefined = isQueryDefined

    @isEidsCollecting.setter
    def isEidsCollecting(self, isEidsCollecting):
        self._isEidsCollecting = isEidsCollecting

    @isEidsCollected.setter
    def isEidsCollected(self, isEidsCollected):
        self._isEidsCollected = isEidsCollected

    @isDataCollected.setter
    def isDataCollected(self, isDataCollected):
        self._isDataCollected = isDataCollected

    @isDataCollecting.setter
    def isDataCollecting(self, isDataCollecting):
        self._isDataCollecting = isDataCollecting

    @isTestdata.setter
    def isTestdata(self, isTestdata):
        self._isTestdata = isTestdata

    @isScivalData.setter
    def isScivalData(self, isScivalData):
        self._isScivalData = isScivalData

    @isEidslist.setter
    def isEidslist(self, isEidslist):
        self._isEidslist = isEidslist

    @isQueryRun.setter
    def isQueryRun(self, isQueryRun):
        self._isQueryRun = isQueryRun

    @isIndexPresent.setter
    def isIndexPresent(self, isIndexPresent):
        self._isIndexPresent = isIndexPresent

    @isReferencesCollecting.setter
    def isReferencesCollecting(self, isReferencesCollecting):
        self._isReferencesCollecting = isReferencesCollecting

    @isReferencesCollected.setter
    def isReferencesCollected(self, isReferencesCollected):
        self._isReferencesCollected = isReferencesCollected

    @property
    def survey_id(self):
        return self._survey_id

    @survey_id.setter
    def survey_id(self, survey_id):
        self._survey_id = survey_id

    @queries.setter
    def queries(self, queries):
        self._queries = queries

    def __init__(self,
                 project_id="",
                 name="",
                 description="",
                 surveyId = "",
                 isQueryDefined=False,
                 isEidsCollecting=False,
                 isEidsCollected=False,
                 isDataCollected=False,
                 isDataCollecting=False,
                 isTestdata=False,
                 isScivalData=False,
                 isEidslist=False,
                 isQueryRun=False,
                 isIndexPresent=False,
                 isReferencesCollecting=False,
                 isReferencesCollected=False,
                 survey_id='',
                 queries=None
                 ):
        self._project_id = project_id
        self._name = name
        self._isQueryDefined = isQueryDefined
        self._isEidsCollecting = isEidsCollecting
        self._isEidsCollected = isEidsCollected
        self._isDataCollected = isDataCollected
        self._isDataCollecting = isDataCollecting
        self._isTestdata = isTestdata
        self._survey_id = surveyId
        self._description = description
        self._isScivalData = isScivalData
        self._isEidslist = isEidslist
        self._isQueryRun = isQueryRun
        self._isIndexPresent = isIndexPresent
        self._isReferencesCollecting = isReferencesCollecting
        self._isReferencesCollected = isReferencesCollected
        self._survey_id = survey_id
        if queries is None:
            self._queries = []
        else:
            self._queries = queries

    def add_query(self, query):
        self._queries.append(query)

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
