from ctypes import CDLL
from .log import TDLog
from .client import TDClient


class TD:

    def __init__(self, td_lib: str or CDLL, log: TDLog=None, client: TDClient=None):
        self.td_lib = td_lib
        self._client = client if client is not None else TDClient(self.td_lib)
        self._log = log if log is not None else TDLog(self.td_lib)

    @property
    def log(self)-> "TDLog":
        return self._log

    @property
    def client(self) -> "TDClient":
        return self._client

    def close(self):
        self.client.__del__()

    def __del__(self):
        self.close()
