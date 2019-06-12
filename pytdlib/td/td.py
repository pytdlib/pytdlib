from ctypes import CDLL
import pytdlib
from .log import TDLog
from .client import TDClient


class TD:
    """
    TDLib instance

    Parameters:
        td_lib (``str`` | `CDLL`)
            TDLib library or path of TDLib library
        log (:class:`TDLog`, *optional*)
            Log for interaction with a TDLib instance Log functions, default is None
        client (:class:`TDClient`, *optional*)
            Client for interaction with a TDLib instance Client functions, default is None
    """
    def __init__(self, td_lib: str or CDLL, log: TDLog=None, client: TDClient=None):
        self.td_lib = td_lib if isinstance(td_lib, CDLL) else CDLL(td_lib)
        self._client = client if client is not None else TDClient(self.td_lib)
        self._log = log if log is not None else TDLog(self.td_lib)

    @property
    def log(self)-> "TDLog":
        return self._log

    @property
    def client(self) -> "TDClient":
        return self._client

    def new_client(self, client_id: int=None):
        """Creates new :class:`TDClient`

        Parameter:
            client_id (``int``, *optional*)
                client identifier, if None new client identifier will use, default is None

        Returns:
            :class:`TDClient`: new TDLib client
        """
        return TDClient(self.td_lib, client_id=client_id)

    def new_app(self, tdjson: str or CDLL=None, **kwargs):
        """Creates new :class:`TDClient`

        Parameters:
            tdjson (``int``, *optional*)
                TDLib library or path of TDLib library,
                if None, default TDLib library of class will be used.
            **kwargs
                Arbitrary keyword arguments.

        Returns:
            :class:`TDClient`: new TDLib client
        """
        return pytdlib.Telegram(tdjson=tdjson if tdjson is not None else self.td_lib, **kwargs)

    def close(self):
        """Closing TDLib interaction client"""
        self.client.__del__()

    def __del__(self):
        self.close()
