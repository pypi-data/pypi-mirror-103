import json


class FromJson:
    def __init__(self, payload):
        self.__dict__ = json.loads(payload)
