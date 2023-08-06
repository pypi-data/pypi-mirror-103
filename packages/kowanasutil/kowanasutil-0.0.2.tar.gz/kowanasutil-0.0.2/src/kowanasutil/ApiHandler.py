import json
from abc import ABCMeta
from .ApiResult import ApiResult

class ApiHandler(metaclass=ABCMeta):
    def handle(self, api, args):
        if args['type'] == 'read':
            return self._handleRead(api, args)
        else:
            return self._handle(api, args)

    def handlePost(self, api, args):
        if args['type'] == 'create':
            return self._handleCreate(api, args)
        else:
            return self._handlePost(api, args)

    def _handle(self, api, args):
        pass

    def _handlePost(self, api, args):
        pass

    def _handleCreate(self, api, args):
        pass

    def _handleUpdate(self, api, args):
        pass

    def _handleRead(self, api, args):
        pass

    def _handleDelete(self, api, args):
        pass

    def _createResult(self, success = True, data = []):
        result = ApiResult(success = success)
        result.update('data', data)
        return result
