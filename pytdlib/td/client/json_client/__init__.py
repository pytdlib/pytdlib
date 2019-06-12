from ctypes import CDLL
from .json_client import Receive, Send, Execute, Destroy, Create


class TDJsonClient(Create, Receive, Send, Execute, Destroy):
    """This class represents initialized Python wrapper for library client functions.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._tdjson = td_json_library
        self._init()

    def _init(self):
        Create.__init__(self, self._tdjson)
        Receive.__init__(self, self._tdjson)
        Send.__init__(self, self._tdjson)
        Execute.__init__(self, self._tdjson)
        Destroy.__init__(self, self._tdjson)
        # super(TDClient, self).__init__(td_json_library)

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
