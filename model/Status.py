class Status:

    @property
    def status(self):
        return self._status

    @property
    def progress(self):
        return self._progress

    @property
    def total(self):
        return self._total

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    @status.setter
    def status(self, status):
        self._status = status

    @progress.setter
    def progress(self, progress):
        self._progress = progress

    @total.setter
    def total(self, total):
        self._total = total

    def __init__(self, status, progress=0, total=0, message=''):
        self._status = status
        self._progress = progress
        self._total = total
        self._message = message

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
