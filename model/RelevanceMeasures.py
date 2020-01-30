class RelevanceMeasure:

    @property
    def recall(self):
        return self._recall

    @property
    def precision(self):
        return self._precision

    @property
    def number_test_entries(self):
        return self._number_test_entries

    @property
    def number_test_entries_found(self):
        return self._number_test_entries_found

    @property
    def number_sample_entries(self):
        return self._number_sample_entries

    @property
    def number_positive_sample_entries(self):
        return self._number_positive_sample_entries

    @property
    def number_of_search_results(self):
        return self._number_of_search_results

    @recall.setter
    def recall(self, recall):
        self._recall = recall

    @precision.setter
    def precision(self, precision):
        self._precision = precision

    @number_test_entries.setter
    def number_test_entries(self, number_test_entries):
        self._number_test_entries = number_test_entries

    @number_test_entries_found.setter
    def number_test_entries_found(self, number_test_entries_found):
        self._number_test_entries_found = number_test_entries_found

    @number_sample_entries.setter
    def number_sample_entries(self, number_sample_entries):
        self._number_sample_entries = number_sample_entries

    @number_positive_sample_entries.setter
    def number_positive_sample_entries(self, number_positive_sample_entries):
        self._number_positive_sample_entries = number_positive_sample_entries

    @number_of_search_results.setter
    def number_of_search_results(self, number_of_search_results):
        self._number_of_search_results = number_of_search_results

    def __init__(self,
                 recall=0,
                 precision=0,
                 number_test_entries=0,
                 number_test_entries_found=0,
                 number_sample_entries=0,
                 number_positive_sample_entries=0,
                 number_of_search_results=0):
        self._recall = recall
        self._precision = precision
        self._number_test_entries = number_test_entries
        self._number_test_entries_found = number_test_entries_found
        self._number_sample_entries = number_sample_entries
        self._number_positive_sample_entries = number_positive_sample_entries
        self._number_of_search_results = number_of_search_results

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
