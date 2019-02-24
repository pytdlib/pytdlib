from ctypes import CDLL
try:
    import ujson as json
except ImportError:
    import json
from .json_client import TDJsonClient


class TDClient:

    def __init__(self, td_library: CDLL=None, json_client: TDJsonClient=None, client_id: int=None):

        if td_library is not None:
            if json_client is not None:
                raise ValueError("One of tdjson or json_client argument is require")
            self._json_client = TDJsonClient(td_library)
        elif json_client is not None:
            self._json_client = json_client
        else:
            raise ValueError("At least one of tdjson or json_client argument is require")
        self.client_id = None if client_id is not None else client_id

    def create(self, force: bool=False):
        if self.client_id is not None and not force:
            return
        self.client_id = self._json_client.create()
        return self.client_id

    def receive(self, timeout: float = 1.0):
        result = self._json_client.receive(self.client_id, timeout)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result

    def send(self, query: str or dict or bytes):
        if isinstance(query, str):
            query = query.encode('utf-8')
        elif isinstance(query, dict):
            query = json.dumps(query).encode('utf-8')
        self._json_client.send(self.client_id, query)

    def execute(self, query: str or dict or bytes):
        if isinstance(query, str):
            query = query.encode('utf-8')
        elif isinstance(query, dict):
            query = json.dumps(query).encode('utf-8')
        result = self._json_client.execute(self.client_id, query)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result

    def destroy(self):
        return self._json_client.destroy(self.client_id)

    def __del__(self):
        if self.client_id is not None:
            self.destroy()
