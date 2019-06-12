from ctypes import CDLL
from .log import SetLogPath, SetLogSize, SetLogLevel, SetLogErrorCallback


class TDLog(SetLogPath, SetLogSize, SetLogLevel, SetLogErrorCallback):
    """This class represents initialized Python wrapper for library log functions.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._tdjson = td_json_library
        self._init()

    def _init(self):
        SetLogPath.__init__(self, self._tdjson)
        SetLogSize.__init__(self, self._tdjson)
        SetLogLevel.__init__(self, self._tdjson)
        SetLogErrorCallback.__init__(self, self._tdjson)

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
