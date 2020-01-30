class Timerange:

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def field(self):
        return self._field

    def __init__(self, start, end, field):
        self._start = start
        self._end = end
        self._field = field

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}
