import time
import logging
import inspect

from signal import signal, SIGINT, SIGTERM, SIGABRT
from threading import Thread
from .types.proxy import HttpProxy, Socks5Proxy, MTprotoProxy
from pytdlib.utils import authorization_stats
from pytdlib import Error
from pytdlib.td import TDLog, TDClient
from pytdlib.api import Object
from ctypes import CDLL
from .types import ProxyType
import os
from .utils import BaseTelegram, Result, MsgId, Callback
from .events import Update
from .dispatcher import Dispatcher
from configparser import ConfigParser
from .methods import Methods

__log__ = logging.getLogger(__name__)


class Telegram(Methods, BaseTelegram):

    EVENTS_WORKERS = 5
    RECEIVE_WORKERS = 1
    MAX_RETRIES = 5
    WAIT_TIMEOUT = 10

    def __init__(self,
                 tdjson: str or CDLL=None,
                 profile: str = "example",
                 api_id: int = None,
                 api_hash: str = None,
                 app_version: str = None,
                 device_model: str = None,
                 system_version: str = None,
                 lang_code: str = None,
                 test_mode: bool = None,
                 use_file_db: bool = None,
                 storage_optimizer: bool = None,
                 file_readable_names: bool = None,
                 use_chat_db: bool = None,
                 use_message_db: bool = None,
                 allow_secret_chat: bool = None,
                 work_dir: str = "",
                 log_name: str = None,
                 log_verbosity: int = 0,
                 bot_token: str = None,
                 phone_number: str = None,
                 phone_code: str or callable = None,
                 password: str = None,
                 force_sms: bool = False,
                 first_name: str = None,
                 last_name: str = None,
                 encryption_key: str = "Naji2nam",
                 workers: int = 4,
                 cb_workers: int=4,
                 config_file: str = "./config.ini",
                 proxy: ProxyType = None,
                 log: TDLog=None,
                 client: TDClient=None):
        super(Telegram, self).__init__()

        if tdjson:
            self._tdjosn = tdjson if isinstance(tdjson, CDLL) else CDLL(tdjson)
        elif client is not None:
            self._tdjosn = client._tdjson
        elif log is not None:
            self._tdjosn = log._tdjson
        else:
            raise ValueError("should have at most one argument of both bot_token or phone_number")

        self._client = TDClient(self._tdjosn) if client is None else client

        self.profile = profile

        self.api_id = api_id
        self.api_hash = api_hash
        self.app_version = app_version
        self.device_model = device_model
        self.system_version = system_version
        self.lang_code = lang_code
        self.test_mode = test_mode
        self.use_file_db = use_file_db
        self.storage_optimizer = storage_optimizer
        self.file_readable_names = file_readable_names
        self.use_chat_db = use_chat_db
        self.use_message_db = use_message_db
        self.allow_secret_chat = allow_secret_chat

        self.work_dir = work_dir

        self.log_name = log_name
        self.log_verbosity = log_verbosity
        self._log = TDLog(self._tdjosn) if log is None else log
        self._log.set_verbosity_level(log_verbosity)

        self.bot_token = bot_token
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.password = password
        self.force_sms = force_sms
        self.first_name = first_name
        self.last_name = last_name

        if self.bot_token and self.phone_number:
            raise ValueError("both bot_token and phone_number can not be used")

        self.encryption_key = encryption_key

        self._proxy = proxy

        self.config_file = config_file

        self.cb_workers = cb_workers

        self.dispatcher = Dispatcher(self, workers)

    @property
    def client(self)-> "TDClient":
        return self._client

    @property
    def log(self)-> "TDLog":
        return self._log

    def connect(self):

        if self._is_connected:
            raise ConnectionError("Client has already been Connected")

        self.load_config()

        self._is_connected = True

        self._client.create()

        option = self._client.receive(1.0)
        option = Object.read(option)
        try:
            assert option.value.value == self.LIB_TD_JSON_VERSION
        except AssertionError:
            raise ValueError('libtdjson >= 1.4.0 is required')
        except AttributeError:
            pass

        for i in range(self.RECEIVE_WORKERS):
            self._receive_worker_list.append(
                Thread(
                    target=self.receive_worker,
                    name="ReceiveWorker#{}".format(i + 1)
                )
            )

            self._receive_worker_list[-1].start()

        for i in range(self.EVENTS_WORKERS):
            self._events_workers_list.append(
                Thread(
                    target=self.events_worker,
                    name="EventsWorker#{}".format(i + 1)
                )
            )

            self._events_workers_list[-1].start()

        for i in range(self.cb_workers):
            self._callback_workers_list.append(
                Thread(
                    target=self.callback_worker,
                    name="CallbackWorker#{}".format(i + 1)
                )
            )

            self._callback_workers_list[-1].start()

        self.authorization(authorization_stats[1])

        return self

    def start(self):

        self.connect()

        if self._is_started:
            raise ConnectionError("Client has already been Started")

        self._is_started = True

        if self._proxy is not None:
            self.add_proxy(self._proxy)

        self.authorization(authorization_stats[-1])

        self.dispatcher.start()

        return self

    def restart(self):
        self.stop()
        self.start()

    def idle(self, func: callable=None, stop_signals: tuple = (SIGINT, SIGTERM, SIGABRT)):

        if func is None:

            self._is_idle = True

            def signal_handler(*_args):
                self._is_idle = False

            for s in stop_signals:
                signal(s, signal_handler)

            while self._is_idle:
                time.sleep(1)
        else:
            func()

        self.stop()

    def run(self, func: callable=None):
        self.start()
        self.idle(func=func)

    def disconnect(self):
        if not self._is_connected:
            raise ConnectionError("Client is already disconnected")

        self._is_connected = False

        for _ in range(self.EVENTS_WORKERS):
            self._recv_queue.put(None)

        for i in self._events_workers_list:
            i.join()

        self._events_workers_list.clear()

        for _ in range(self.cb_workers):
            self._callback_queue.put(None)

        for i in self._callback_workers_list:
            i.join()

        self._callback_workers_list.clear()

        self._client.destroy()

        return self

    def stop(self):

        if not self._is_started:
            raise ConnectionError("Client is already stopped")

        self._is_started = False

        self.dispatcher.stop()

        self.disconnect()

        return self

    def receive_worker(self):

        while self._is_connected:
            event = self._client.receive(1.0)

            if event is not None:
                self._recv_queue.put(event)

    def process_event(self, event: dict):
        msg_id = event["@extra"] if "@extra" in event else None

        event = Object.read(event)

        if msg_id in self._results:
            self._results[msg_id].value = event
            self._results[msg_id].event.set()
        elif msg_id in self._cresults:
            cb = self._cresults.pop(msg_id)
            cb.result = event
            cb.event.set()
            self._callback_queue.put(cb)
        else:
            if event.ID == 'updates':
                for update in event.updates:
                    self.dispatcher.events_queue.put(update)
            else:
                self.dispatcher.events_queue.put(event)

    def events_worker(self):
        while True:
            event = self._recv_queue.get()
            if event is None:
                break

            self.process_event(event)

    def callback_worker(self):
        while True:
            callback = self._callback_queue.get()
            if callback is None:
                break
            try:
                callback.run()
            except:
                pass

    def _send(self, data: Object, msg_id: int):

        self._results[msg_id] = Result()

        self._client.send(data)

        self._results[msg_id].event.wait(self.WAIT_TIMEOUT)
        result = self._results.pop(msg_id).value

        if result is None:
            raise TimeoutError
        elif isinstance(result, Object.all["error"]):
            raise Error(result.code, result.message)
        else:
            return result

    def send(self, data: Object, response: Callback=True, retries: int = MAX_RETRIES) -> "Callback or Object":
        if not response:
            return self._client.send(data)
        else:
            msg_id = MsgId()
            data.extra = msg_id
            if isinstance(response, Callback):
                self._cresults[msg_id] = response
                self._client.send(data)
                return self._cresults[msg_id]
            else:
                for _ in range(1, retries + 1):
                    try:
                        return self._send(data, msg_id)
                    except (OSError, TimeoutError) as e:
                        if _ == retries:
                            raise e from None

    def on(self, event: Update=None):

        def decorator(func: callable) -> Update:
            if isinstance(func, Update):
                func = func.callback

            event_handler = self._event_cb(event, func)

            if not isinstance(self, Update):
                self.add_event_handler(event_handler)

            return event_handler

        return decorator

    @staticmethod
    def _event_cb(event: Update, cb: callable) -> Update:
        if isinstance(event, type):
            event = event(callback=cb)
        else:
            event.callback = cb
        return event

    def add_event_handler(self, event: Update):

        if event.callback is None:
            raise AttributeError("No Callback Function Found")

        self.dispatcher.add_event(event)

    def remove_event_handler(self, event: Update):
        return self.dispatcher.remove_event(event)

    def load_config(self):
        parser = ConfigParser()
        parser.read(self.config_file)
        has_section = parser.has_section("tdlib")

        attributes = [a[0] for a in inspect.getmembers(BaseTelegram, lambda a: not (inspect.isroutine(a)))
                      if not a[0].startswith('_')] + ["API_ID", "API_HASH"]
        for attribute in attributes:
            option = attribute.lower()
            value = getattr(self, option, None)
            if value is None:
                if has_section:
                    value = parser.get(self._section_name, option, fallback=None)
                setattr(self, option, value if value is not None else getattr(Telegram, attribute, None))

        if not (self.api_id and self.api_hash):
            raise AttributeError(
                "No API Key found. "
                "More info: https://docs.pyrogram.ml/start/ProjectSetup#configuration"
            )

        if not self.work_dir or self.work_dir == self.WORK_DIR:
            self.work_dir = os.path.join(os.getcwd(), self.profile)

        if not self._proxy and parser.has_section("proxy"):
            proxies = {
                "http": (HttpProxy, {"username", "password", "http_only"}),
                "socks": (Socks5Proxy, {"username", "password"}),
                "mtproto": (MTprotoProxy, ["secret"])
            }
            proxy_type = parser.get("proxy", "type", fallback=None)
            proxy, ext_args = proxies.get(proxy_type, (None, None))
            if proxy:
                enabled = parser.getboolean("proxy", "enabled", fallback=True)
                hostname = parser.get("proxy", "hostname")
                port = parser.getint("proxy", "port")
                args = {"hostname": hostname, "port": port, "enabled": enabled}
                for ext_arg in ext_args:
                    args[ext_arg] = parser.get("proxy", ext_arg, fallback=None) or None

                self._proxy = proxy(**args)
            else:
                raise ValueError('ProxyType {} Not Found'.format(proxy_type))

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()
