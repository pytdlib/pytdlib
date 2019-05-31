import platform
from queue import Queue
from pytdlib import __version__


class BaseTelegram:
    APP_VERSION = str(__version__)
    DEVICE_MODEL = "{} {}".format(
        platform.python_implementation(),
        platform.python_version()
    )
    SYSTEM_VERSION = "{} {}".format(
        platform.system(),
        platform.release()
    )
    LANG_CODE = "en"
    TEST_MODE = False
    USE_FILE_DB = True
    STORAGE_OPTIMIZER = True
    FILE_READABLE_NAMES = True
    USE_CHAT_DB = True
    USE_MESSAGE_DB = True
    ALLOW_SECRET_CHAT = False
    WORK_DIR = "."

    LIB_TD_JSON_VERSION = '1.4.0'
    _section_name = "tdlib"

    def __init__(self):
        self._is_started = False
        self._is_connected = False
        self._is_idle = None
        self._authorized = False
        self._recv_queue = Queue()
        self._callback_queue = Queue()

        self._events_workers_list = []
        self._receive_worker_list = []
        self._callback_workers_list = []
        self._results = {}
        self._cresults = {}

        self.api_id = None
        self.api_hash = None
        self.app_version = None
        self.device_model = None
        self.system_version = None
        self.lang_code = None
        self.test_mode = None
        self.use_file_db = None
        self.storage_optimizer = None
        self.file_readable_names = None
        self.use_chat_db = None
        self.use_message_db = None
        self.allow_secret_chat = None

        self.work_dir = None

        self.bot_token = None
        self.phone_number = None
        self.phone_code = None
        self.password = None
        self.force_sms = None
        self.first_name = None
        self.last_name = None

        self.encryption_key = None

        self._proxy = None

    def send(self, data: object, callback: bool = None):
        pass
