from ctypes import CDLL
from .log import SetLogPath, SetLogSize, SetLogLevel, SetLogErrorCallback


class TDLog(SetLogPath, SetLogSize, SetLogLevel, SetLogErrorCallback):
    """This class represents initialized Python wrapper for library log functions."""
    def __init__(self, tdjson: CDLL):
        SetLogPath.__init__(self, tdjson)
        SetLogSize.__init__(self, tdjson)
        SetLogLevel.__init__(self, tdjson)
        SetLogErrorCallback.__init__(self, tdjson)

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
