from ctypes import CDLL, c_void_p, c_char_p, c_double


class Create:

    def __init__(self, td_json_library: CDLL):
        self._td_json_client_create = td_json_library.td_json_client_create
        self._td_json_client_create.restype = c_void_p
        self._td_json_client_create.argtypes = []

    def create(self) -> int:
        """
        Creates a new instance of TDLib.
        """
        return self._td_json_client_create()

    def __call__(self) -> int:
        return self.create()


class Receive:

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
        """
        return self._td_json_client_receive(client_id, timeout)

    def __call__(self, client_id: int, timeout: float = 1.0) -> bytes:
        return self.receive(client_id, timeout)


class Send:

    def __init__(self, td_json_library: CDLL):
        self._td_json_client_send = td_json_library.td_json_client_send
        self._td_json_client_send.restype = None
        self._td_json_client_send.argtypes = [c_void_p, c_char_p]

    def send(self, client_id: int, req: bytes):
        """
        Sends request to the TDLib client. May be called from any thread.
        """
        return self._td_json_client_send(client_id, req)

    def __call__(self, client_id: int, req: bytes):
        return self._td_json_client_send(client_id, req)


class Execute:

    def __init__(self, td_json_library: CDLL):
        self._td_json_client_execute = td_json_library.td_json_client_execute
        self._td_json_client_execute.restype = c_char_p
        self._td_json_client_execute.argtypes = [c_void_p, c_char_p]

    def execute(self, client_id: int, req: bytes) -> bytes:
        """
        Synchronously executes TDLib request. May be called from any thread.
        Only a few requests can be executed synchronously.
        Returned pointer will be deallocated by TDLib during next call in the same
        thread, so it can't be used after that.
        """
        return self._td_json_client_execute(client_id, req)

    def __call__(self, client_id: int, req: bytes) -> bytes:
        return self.execute(client_id, req)


class Destroy:

    def __init__(self, td_json_library: CDLL):
        self._td_json_client_destroy = td_json_library.td_json_client_destroy
        self._td_json_client_destroy.restype = None
        self._td_json_client_destroy.argtypes = [c_void_p]

    def destroy(self, client_id: int):
        """
        Destroys the TDLib client instance. After this is called the client
        instance shouldn't be used anymore.
        """
        return self._td_json_client_destroy(client_id)

    def __call__(self, client_id: int):
        return self.destroy(client_id)
