from model.SdgSlice import SdgSlice


class SdgWheel:

    @property
    def grey_slices(self):
        return self._grey_slices

    @property
    def colored_slices(self):
        return self._colored_slices

    @property
    def factors(self):
        return self._wheel

    def __init__(self, wheel):
        self._wheel = wheel
        self._grey_slices = []
        self._colored_slices = []
        for index, percentage in enumerate(wheel):
            self._grey_slices.append(SdgSlice(index, 1, True))
            self._colored_slices.append(SdgSlice(index, percentage, False))
