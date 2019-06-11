class UpdateContainer:

    def __init__(self, update):
        self._doc = update

    def __getstate__(self):
        return self.__dict__.copy()
