from ctypes import (CDLL, c_int, c_char_p, c_longlong, CFUNCTYPE)


class SetLogPath:
    """This class represents initialized Python wrapper for library log td_set_log_file_path functions.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._td_set_file_path = td_json_library.td_set_log_file_path
        self._td_set_file_path.restype = c_int
        self._td_set_file_path.argtypes = [c_char_p]

    def set_file_path(self, path: bytes):
        """
        Sets the path to the file where the internal TDLib log will be written.
        By default TDLib writes logs to stderr or an OS specific log. Use this method
        to write the log to a file instead.

        Parameters:
            path (``bytes``)
                path to the file where the internal TDLib log will be written
        """
        return self._td_set_file_path(path)

    __call__ = set_file_path


class SetLogSize:
    """This class represents initialized Python wrapper for library log td_set_log_max_file_size functions.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._td_set_max_file_size = td_json_library.td_set_log_max_file_size
        self._td_set_max_file_size.restype = None
        self._td_set_max_file_size.argtypes = [c_longlong]

    def set_max_file_size(self, size: int):
        """
        Sets maximum size of the file to where the internal TDLib log is written before
        the file will be auto-rotated. Unused if log is not written to a file. Defaults
        to 10 MB.

        Parameters:
            size (``int``)
                maximum size of the file to where the internal TDLib log is written
        """
        return self._td_set_max_file_size(size)

    __call__ = set_max_file_size


class SetLogLevel:

    def __init__(self, td_json_library: CDLL):
        """This class represents initialized Python wrapper for library log td_set_log_verbosity_level functions.

        Parameters:
            td_json_library (:obj:`CDLL`)
                TDLib library
        """
        self._td_set_verbosity_level = td_json_library.td_set_log_verbosity_level
        self._td_set_verbosity_level.restype = None
        self._td_set_verbosity_level.argtypes = [c_int]

    def set_verbosity_level(self, level: int):
        """
        Sets the verbosity level of the internal logging of TDLib. By default the
        TDLib uses a log verbosity level of 5.

        Parameters:
            level (``int``)
                verbosity level of the internal logging of TDLib
        """
        return self._td_set_verbosity_level(level)

    __call__ = set_verbosity_level


class SetLogErrorCallback:

    def __init__(self, td_json_library: CDLL):
        """This class represents initialized Python wrapper for library log td_set_fatal_error_callback functions.

        Parameters:
            td_json_library (:obj:`CDLL`)
                TDLib library
        """
        self._td_set_fatal_error_callback = td_json_library.td_set_log_fatal_error_callback
        self._td_fatal_error_callback_type = CFUNCTYPE(None, c_char_p)
        self._td_set_fatal_error_callback.restype = None
        self._td_set_fatal_error_callback.argtypes = [self._td_fatal_error_callback_type]

    def set_fatal_error_callback(self,  callback: callable):
        """
        Sets the callback that will be called when a fatal error happens. None of the TDLib
        methods can be called from the callback. The TDLib will crash as soon as callback returns.
        By default the callback is not set.

        Parameters:
            callback (``callable``)
                callback that will be called when a fatal error happens
        """
        return self._td_set_fatal_error_callback(self._td_fatal_error_callback_type(callback))

    __call__ = set_fatal_error_callback
