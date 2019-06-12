from ctypes import CDLL, c_void_p, c_char_p, c_double


class Create:
    """This class represents initialized Python wrapper for library client create method.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._td_json_client_create = td_json_library.td_json_client_create
        self._td_json_client_create.restype = c_void_p
        self._td_json_client_create.argtypes = []

    def create(self) -> int:
        """
        Creates a new instance of TDLib.

        Returns:
            ``int``: New client instance identifier
        """
        return self._td_json_client_create()

    __call__ = create


class Receive:
    """This class represents initialized Python wrapper for library client receive method.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._td_json_client_receive = td_json_library.td_json_client_receive
        self._td_json_client_receive.restype = c_char_p
        self._td_json_client_receive.argtypes = [c_void_p, c_double]

    def receive(self,  client_id: int, timeout: float = 1.0) -> bytes:
        """
        Receives incoming updates and request responses from the TDLib client.
        May be called from any thread, but shouldn't be called simultaneously from two
        different threads. Returned pointer will be deallocated by TDLib during next call in the same thread, so it
        can't be used after that.

        Parameters:
            client_id (``int``)
                Client identifier
            timeout (``float``)
                time out for receive method, default is 1.0

        Returns:
            ``bytes``: Incoming updates or request responses on success
        """
        return self._td_json_client_receive(client_id, timeout)

    __call__ = receive


class Send:
    """This class represents initialized Python wrapper for library client send method.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._td_json_client_send = td_json_library.td_json_client_send
        self._td_json_client_send.restype = None
        self._td_json_client_send.argtypes = [c_void_p, c_char_p]

    def send(self, client_id: int, req: bytes):
        """
        Sends request to the TDLib client. May be called from any thread.

        Parameters:
            client_id (``int``)
                Client identifier
            req (``bytes``)
                Request query
        """
        return self._td_json_client_send(client_id, req)

    __call__ = send


class Execute:
    """This class represents initialized Python wrapper for library client execute method.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._td_json_client_execute = td_json_library.td_json_client_execute
        self._td_json_client_execute.restype = c_char_p
        self._td_json_client_execute.argtypes = [c_void_p, c_char_p]

    def execute(self, req: bytes, client_id: int=None) -> bytes:
        """
        Synchronously executes TDLib request. May be called from any thread.
        Only a few requests can be executed synchronously.
        Returned pointer will be deallocated by TDLib during next call in the same
        thread, so it can't be used after that.

        Parameters:
            req (``bytes``)
                Request query
            client_id (``int``, *optional*)
                Client identifier

        Returns:
            ``bytes``: Result of request
        """
        return self._td_json_client_execute(client_id, req)

    __call__ = execute


class Destroy:
    """This class represents initialized Python wrapper for library client destroy method.

    Parameters:
        td_json_library (:obj:`CDLL`)
            TDLib library
    """
    def __init__(self, td_json_library: CDLL):
        self._td_json_client_destroy = td_json_library.td_json_client_destroy
        self._td_json_client_destroy.restype = None
        self._td_json_client_destroy.argtypes = [c_void_p]

    def destroy(self, client_id: int):
        """
        Destroys the TDLib client instance. After this is called the client
        instance shouldn't be used anymore.

        Parameters:
            client_id (``int``)
                Client identifier
        """
        return self._td_json_client_destroy(client_id)

    __call__ = destroy
