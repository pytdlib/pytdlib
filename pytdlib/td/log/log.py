from ctypes import (CDLL, c_int, c_char_p, c_longlong, CFUNCTYPE)


class SetLogPath:

    def __init__(self, td_library: CDLL):
        self._td_set_file_path = td_library.td_set_log_file_path
        self._td_set_file_path.restype = c_int
        self._td_set_file_path.argtypes = [c_char_p]

    def set_file_path(self, path: str):
        """
        Sets the path to the file where the internal TDLib log will be written.
        By default TDLib writes logs to stderr or an OS specific log. Use this method
        to write the log to a file instead.
        """
        return self._td_set_file_path(path)

    def __call__(self, path: str):
        return self.set_file_path(path)


class SetLogSize:

    def __init__(self, td_library: CDLL):
        self._td_set_max_file_size = td_library.td_set_log_max_file_size
        self._td_set_max_file_size.restype = None
        self._td_set_max_file_size.argtypes = [c_longlong]

    def set_max_file_size(self, size: int):
        """
        Sets maximum size of the file to where the internal TDLib log is written before
        the file will be auto-rotated. Unused if log is not written to a file. Defaults
        to 10 MB.
        """
        return self._td_set_max_file_size(size)

    def __call__(self, size: int):
        return self.set_max_file_size(size)


class SetLogLevel:

    def __init__(self, td_library: CDLL):
        self._td_set_verbosity_level = td_library.td_set_log_verbosity_level
        self._td_set_verbosity_level.restype = None
        self._td_set_verbosity_level.argtypes = [c_int]

    def set_verbosity_level(self, level: int):
        """
        Sets the verbosity level of the internal logging of TDLib. By default the
        TDLib uses a log verbosity level of 5.
        """
        return self._td_set_verbosity_level(level)

    def __call__(self, level: int):
        return self.set_verbosity_level(level)


class SetLogErrorCallback:

    def __init__(self, td_library: CDLL):
        self._td_set_fatal_error_callback = td_library.td_set_log_fatal_error_callback
        self._td_fatal_error_callback_type = CFUNCTYPE(None, c_char_p)
        self._td_set_fatal_error_callback.restype = None
        self._td_set_fatal_error_callback.argtypes = [self._td_fatal_error_callback_type]

    def set_fatal_error_callback(self, func: callable):
        """
        Sets the callback that will be called when a fatal error happens. None of the TDLib
        methods can be called from the callback. The TDLib will crash as soon as callback returns.
        By default the callback is not set.
        """
        return self._td_set_fatal_error_callback(self._td_fatal_error_callback_type(func))

    def __call__(self, func: callable):
        return self.set_fatal_error_callback(func)
