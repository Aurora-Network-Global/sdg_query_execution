import json


class HiddenEncoder(json.JSONEncoder):
    """A decoder, that uses the hidden properties of a class for serialization"""
    def default(self, o):
        return {k.lstrip('_'): v for k, v in o.__getstate__().items()}
