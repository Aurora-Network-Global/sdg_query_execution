class ScivalUpdate:

    def __init__(self, scival_data):
        self.scival_data = scival_data

    def __getstate__(self):
        return self.__dict__.copy()
