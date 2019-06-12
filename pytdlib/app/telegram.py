import time
import logging
from ctypes import CDLL
import threading
from configparser import ConfigParser
from signal import signal, SIGINT, SIGTERM, SIGABRT

from pytdlib.utils import AuthorizationStats
from pytdlib.api import Object
from pytdlib.api.errors import TLError
from pytdlib.td.client import TDClient
from pytdlib.app.events import Update

from .types import ProxyType, HttpProxy, Socks5Proxy, MTprotoProxy
from .ext import BaseTelegram, TdlibParameters, Dispatcher, Result, MsgId, Callback, LogStream
from .options import TLOptions, Options
from .methods import Methods

log = logging.getLogger(__name__)


class Telegram(Methods, BaseTelegram):

    EVENTS_WORKERS = 5
    RECEIVE_WORKERS = 1
    MAX_RETRIES = 5
    WAIT_TIMEOUT = 10
    PROFILE = 'tdlib_account'

    def __init__(self,
                 tdjson: str or CDLL=None,
                 profile: str = PROFILE,
                 tdlib_parameters: TdlibParameters or dict=None,
                 log_stream: LogStream.Default or LogStream.File or LogStream.Empty = None,
                 log_verbosity: int = 0,
                 bot_token: str = None,
                 phone_number: str = None,
                 phone_code: str or callable = None,
                 password: str = None,
                 force_sms: bool = False,
                 first_name: str = None,
                 last_name: str = None,
                 encryption_key: str = 'Naji2nam',
                 workers: int = 4,
                 cb_workers: int=4,
                 config_file: str = './config.ini',
                 proxy: ProxyType = None,
                 options: Options or dict = None,
                 client: TDClient=None,):
        super(Telegram, self).__init__()

        if tdjson is not None:
            self._tdjosn = tdjson if isinstance(tdjson, CDLL) else CDLL(tdjson)
        elif client is not None:
            self._tdjosn = client._tdjson
        else:
            raise ValueError('should have at most one argument of both bot_token or phone_number')

        self._client = TDClient(self._tdjosn) if client is None else client

        self.profile = profile

        if tdlib_parameters is not None:
            self.tdlib_parameters = tdlib_parameters

        self.log_stream = log_stream
        self.log_verbosity = log_verbosity

        self.bot_token = bot_token
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.password = password
        self.force_sms = force_sms
        self.first_name = first_name
        self.last_name = last_name

        if self.bot_token and self.phone_number:
            raise ValueError('both bot_token and phone_number can not be used')

        self.encryption_key = encryption_key

        self._proxy = proxy

        self.config_file = config_file

        self.cb_workers = cb_workers

        self.dispatcher = Dispatcher(self, workers)

        self.options_dict = {name: value for name, value in vars(options).items()
                             if value is not None} if options is not None else {}

        self.options = TLOptions(self.set_option, self.get_option)

    @property
    def client(self)-> 'TDClient':
        return self._client

    def connect(self):

        if self._is_connected:
            raise ConnectionError('Client has already been Connected')

        log.info('Connecting ...')

        self.load_config()

        self._is_connected = True

        options_dict = self.options_dict.copy()
        try:
            for i in range(self.RECEIVE_WORKERS):
                self._receive_worker_list.append(
                    threading.Thread(
                        target=self.receive_worker,
                        name='ReceiveWorker#{}'.format(i + 1)
                    )
                )

                self._receive_worker_list[-1].start()

            for i in range(self.EVENTS_WORKERS):
                self._events_workers_list.append(
                    threading.Thread(
                        target=self.events_worker,
                        name='EventsWorker#{}'.format(i + 1)
                    )
                )

                self._events_workers_list[-1].start()

            for i in range(self.cb_workers):
                self._callback_workers_list.append(
                    threading.Thread(
                        target=self.callback_worker,
                        name='CallbackWorker#{}'.format(i + 1)
                    )
                )

                self._callback_workers_list[-1].start()

        except Exception as e:
            self._is_connected = False
            raise e

        assert (self.options.version == self.LIB_TD_JSON_VERSION), 'libtdjson >= 1.4.0 is required'

        log.info('Starting Pre-Authentication.')
        self.authorization(AuthorizationStats(2))
        log.info('Pre-Authentication Done.')

        for name, value in options_dict.items():
            if name not in TLOptions.NOT_WRITEABLE and value is not None:
                try:
                    setattr(self.options, name, value)
                except TLError:
                    pass

        if self._proxy is not None:
            log.info('Set Proxy')
            self.proxy = self._proxy

        log.info('... Connected.')
        return self

    def start(self):

        if not self._is_connected:
            self.connect()

        if self._is_started:
            raise ConnectionError('Client has already been Started')

        log.info('Starting ...')

        self._is_started = True

        try:
            log.info('Starting Main-Authorization.')
            self.authorization(AuthorizationStats(6))
            log.info('Main-Authorization Done.')

            self.dispatcher.start()

        except Exception as e:
            self._is_started = False
            raise e

        log.info('... Started')
        return self

    def restart(self):
        log.info('Restarting App')
        self.stop()
        self._client.create(use=True)
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

        self.close()

    def run(self, func: callable=None):
        self.start()
        self.idle(func=func)

    def disconnect(self):
        if not self._is_connected:
            raise ConnectionError('Client is already disconnected')
        log.info('Disconnecting ...')
        self._is_connected = False

        for _ in range(self.EVENTS_WORKERS):
            self._recv_queue.put(None)

        # for i in self._events_workers_list:
        #    i.join()

        self._events_workers_list.clear()

        for _ in range(self.cb_workers):
            self._callback_queue.put(None)

        for i in self._callback_workers_list:
            i.join()

        self._callback_workers_list.clear()

        self._client.closed()

        log.info('... Disconnected')
        return self

    def stop(self):

        if not self._is_started:
            raise ConnectionError('Client is already stopped')

        log.info('Stopping ...')
        self._is_started = False

        self.dispatcher.stop()

        self.disconnect()

        log.info('... Stopped.')
        return self

    def receive_worker(self):
        name = threading.current_thread().name
        log.debug('%s Started' % name)
        while self._is_connected:
            event = self._client.receive(1.0)

            if event is not None:
                self._recv_queue.put(event)

        log.info('%s Stopped' % name)

    def process_event(self, event: dict):
        msg_id = event['@extra'] if '@extra' in event else None

        event = Object.read(event)

        if event.ID == 'updateAuthorizationState':
            if event.authorization_state.ID == 'authorizationStateLoggingOut':
                self.restart()
            elif event.authorization_state.ID == 'authorizationStateClosing':
                self._is_ready = False
            elif event.authorization_state.ID == 'authorizationStateClosed':
                if self._is_started:
                    self.stop()
        elif event.ID == 'updateOption' and event.value.ID != 'optionValueEmpty':
            self.options_dict[event.name] = event.value.value

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
        name = threading.current_thread().name
        log.debug('%s Started' % name)
        while True:
            event = self._recv_queue.get()
            if event is None:
                break

            self.process_event(event)

        log.info('%s Stopped' % name)

    def callback_worker(self):
        name = threading.current_thread().name
        log.debug('%s Started' % name)
        while True:
            callback = self._callback_queue.get()
            if callback is None:
                break
            try:
                callback.run()
            except Exception as e:
                log.error(e, exc_info=True)

        log.info('%s Stopped' % name)

    def _send(self, data: Object, msg_id: int):

        self._results[msg_id] = Result()

        self._client.send(data.to_bytes())

        self._results[msg_id].event.wait(self.WAIT_TIMEOUT)
        result = self._results.pop(msg_id).value

        if result is None:
            raise TimeoutError
        elif isinstance(result, Object.all['error']):
            raise TLError(result.code, result.message)
        else:
            return result

    def send(self, data: Object, response: Callback=True, retries: int = MAX_RETRIES) -> 'Callback or Object':

        if not response:
            return self._client.send(data.to_bytes())
        else:
            msg_id = MsgId()
            data.extra = msg_id
            if isinstance(response, Callback):
                self._cresults[msg_id] = response
                self._client.send(data.to_bytes())
                return self._cresults[msg_id]
            else:
                for _ in range(1, retries + 1):
                    try:
                        return self._send(data, msg_id)
                    except (OSError, TimeoutError) as e:
                        if _ == retries:
                            raise e from None

    def execute(self, data: Object):
        res = self.client.execute(data.to_bytes())
        return Object.read(res)

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
            raise AttributeError('No Callback Function Found')

        self.dispatcher.add_event(event)

    def remove_event_handler(self, event: Update):
        return self.dispatcher.remove_event(event)

    def load_config(self):
        parser = ConfigParser()
        parser.read(self.config_file)
        log.info('Loading Config File.')
        TdlibParameters.load_from_config(self.tdlib_parameters, self.config_file, self.profile)
        proxy_section_name = self._proxy_section_name
        if self._proxy is None and parser.has_section(proxy_section_name):
            log.info('Proxy Section in Config File.')
            proxies = {
                'http': (HttpProxy, {'username', 'password', 'http_only'}),
                'socks': (Socks5Proxy, {'username', 'password'}),
                'mtproto': (MTprotoProxy, ['secret'])
            }
            proxy_type = parser.get('proxy', 'type', fallback=None)
            proxy, ext_args = proxies.get(proxy_type, (None, None))
            if proxy:
                enabled = parser.getboolean(proxy_section_name, 'enabled', fallback=True)
                hostname = parser.get(proxy_section_name, 'hostname')
                port = parser.getint(proxy_section_name, 'port')
                args = {'hostname': hostname, 'port': port, 'enabled': enabled}
                for ext_arg in ext_args:
                    args[ext_arg] = parser.get('proxy', ext_arg, fallback=None) or None

                self._proxy = proxy(**args)
            else:
                raise ValueError('ProxyType {} Not Found'.format(proxy_type))

    def __enter__(self):
        return self.connect()

    def __exit__(self, *args):
        if self._is_ready:
            self.close()
