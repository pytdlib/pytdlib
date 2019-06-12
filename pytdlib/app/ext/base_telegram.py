from queue import Queue


class BaseTelegram:

    LIB_TD_JSON_VERSION = '1.4.0'
    _proxy_section_name = 'proxy'

    def __init__(self):
        self._is_started = False
        self._is_connected = False
        self._is_idle = None
        self._authorized = False
        self._is_ready = True
        self._recv_queue = Queue()
        self._callback_queue = Queue()

        self._events_workers_list = []
        self._receive_worker_list = []
        self._callback_workers_list = []
        self._results = {}
        self._cresults = {}

        self.tdlib_parameters = {}
        self.bot_token = None
        self.phone_number = None
        self.phone_code = None
        self.password = None
        self.force_sms = None
        self.first_name = None
        self.last_name = None

        self.encryption_key = None

        self.options_dict = {}

        self._proxy = None

    def send(self, data, callback=None, retries=None):
        pass

    def execute(self, data):
        pass

    @property
    def is_authorized(self):
        return self._authorized
