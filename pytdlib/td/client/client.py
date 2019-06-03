from ctypes import CDLL
from .json_client import TDJsonClient
from pytdlib.utils import object_to_bytes, json
import logging

log = logging.getLogger(__name__)


class TDClient:

    def __init__(self, td_library: CDLL=None, json_client: TDJsonClient=None, client_id: int=None):

        if td_library is not None:
            if json_client is not None:
                raise ValueError("One of tdjson or json_client argument is required")
            self._json_client = TDJsonClient(td_library)
        elif json_client is not None:
            self._json_client = json_client
        else:
            raise ValueError("At least one of tdjson or json_client argument is required")
        self.client_id = self.create() if client_id is None else client_id
        log.info('TDClient(%s) Created' % self.client_id)

    @property
    def _tdjson(self)-> "CDLL":
        return self._json_client._tdjson

    def create(self, use: bool=False):
        client_id = self._json_client.create()
        if use:
            self.client_id = client_id
        return client_id

    def receive(self, timeout: float = 1.0):
        result = self._json_client.receive(self.client_id, timeout)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result

    def send(self, query: str or dict or bytes):

        query = object_to_bytes(query)

        self._json_client.send(self.client_id, query)

    def execute(self, query: str or dict or bytes):

        query = object_to_bytes(query)

        result = self._json_client.execute(self.client_id, query)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result

    def destroy(self):
        log.info('TDClient(%s) Destroyed' % self.client_id)
        self._json_client.destroy(self.client_id)
        self.closed()

    def closed(self):
        self.client_id = None

    def __str__(self):
        return '<TDClient(%s)>' % self.client_id

    def __del__(self):
        if self.client_id is not None:
            self.destroy()
