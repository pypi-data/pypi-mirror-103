import json

class ApiResult:
    result = {}

    def __init__(self, success = False):
        self.result['success'] = success

    def toJson(self):
        return json.dumps(self.result)

    def update(self, key, data):
        self.result[key] = data