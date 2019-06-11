class ScivalUpdate:

    def __init__(self, scival_data):
        self._scival_data = scival_data

    def __getstate__(self):
        return self.__dict__.copy()
