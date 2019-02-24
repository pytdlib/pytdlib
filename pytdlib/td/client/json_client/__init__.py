from ctypes import CDLL
from .json_client import Receive, Send, Execute, Destroy, Create


class TDJsonClient(Create, Receive, Send, Execute, Destroy):
    """This class represents initialized Python wrapper for library client functions."""
    def __init__(self, td_json_library: CDLL):
        Create.__init__(self, td_json_library)
        Receive.__init__(self, td_json_library)
        Send.__init__(self, td_json_library)
        Execute.__init__(self, td_json_library)
        Destroy.__init__(self, td_json_library)
        # super(TDClient, self).__init__(td_json_library)

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
