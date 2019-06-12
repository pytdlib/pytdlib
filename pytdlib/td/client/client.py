from ctypes import CDLL
from .json_client import TDJsonClient
from pytdlib.utils import object_to_bytes, json
import logging

log = logging.getLogger(__name__)


class TDClient:
    """
    interface for interaction with a TDLib instance

    Parameters:
        td_library (:obj:`CDLL`)
            TDLib library, can be ignored in case of passing json_client param.
        json_client (:class:`TDJsonClient`, *optional*)
            Wrappered TDLib json client
        client_id (``int``, *optional*)
            Client identifier in case of using default client
    """
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

    @property
    def json_client(self):
        return self._json_client

    def create(self, use: bool=False):
        """Creates a new instance wrapper of TDLib.

        Parameters:
            use (``bool``, *optional*)
               Use of created wrapper, default is False.

        Returns:
            ``int``: Created client identifier
        """
        client_id = self._json_client.create()
        if use:
            self.client_id = client_id
        return client_id

    def receive(self, timeout: float = 1.0) -> dict:
        """
        Receives incoming updates and request responses from the wrapper client.
        May be called from any thread, but shouldn't be called simultaneously from two
        different threads. Returned pointer will be deallocated by TDLib during next call in the same thread, so it
        can't be used after that.

        Parameters:
            timeout (``float``, *optional*)
                Time out for receive method, default is 1.0

        Returns:
            ``bytes``: On success
        """
        result = self._json_client.receive(self.client_id, timeout)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result

    def send(self, query: str or dict or bytes):
        """
        Sends request to the client. May be called from any thread.

        Parameters:
            query (``bytes`` | ``str`` | ``dict``)
                Request query
        """
        query = object_to_bytes(query)

        self._json_client.send(self.client_id, query)

    def execute(self, query: str or dict or bytes) -> dict:
        """
        Synchronously executes TDLib request. May be called from any thread.
        Only a few requests can be executed synchronously.
        Returned pointer will be deallocated by TDLib during next call in the same
        thread, so it can't be used after that.

        Parameters:
            query (``bytes`` | ``str`` | ``dict``)
                Request query

        Returns:
            ``dict``: Result of request
        """
        query = object_to_bytes(query)

        result = self._json_client.execute(query, self.client_id)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result

    def destroy(self):
        """
        Destroys the TDLib client instance. After this is called the client
        instance shouldn't be used anymore.
        """
        log.info('TDClient(%s) Destroyed' % self.client_id)
        self._json_client.destroy(self.client_id)
        self.closed()

    def closed(self):
        """null client_id"""
        self.client_id = None

    def __str__(self):
        return '<TDClient(%s)>' % self.client_id

    def __del__(self):
        if self.client_id is not None:
            self.destroy()
