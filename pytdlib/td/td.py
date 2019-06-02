from ctypes import CDLL
from .log import TDLog
from .client import TDClient
from ..app import Telegram


class TD:

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
        return TDClient(self.td_lib, client_id=client_id)

    def new_app(self, tdjson: str or CDLL=None, **kwargs):
        return Telegram(tdjson=tdjson if tdjson is not None else self.td_lib, **kwargs)

    def close(self):
        self.client.__del__()

    def __del__(self):
        self.close()
