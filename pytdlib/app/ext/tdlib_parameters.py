import os
import inspect
import logging
import platform
from configparser import ConfigParser

from pytdlib import __version__

log = logging.getLogger(__name__)


class TdlibParameters:
    """
     Contains parameters for TDLib initialization

    Parameters:
        api_id (``int``, *optional*)
            api_id Application identifier for Telegram API access, which can be obtained at https://my.telegram.org
        api_hash (``str``, *optional*)
            api_hash Application identifier hash for Telegram API access, which can be obtained at https://my.telegram.org
        app_version (``str``, *optional*)
            app_version Application version; must be non-empty
        device_model (``str``, *optional*)
            device_model Model of the device the application is being run on
        system_version (``str``, *optional*)
            system_version Version of the operating system the application is being run on
        lang_code (``str``, *optional*)
            lang_code IETF language tag of the user's operating system language
        test_mode (``bool``, *optional*)
            test_mode If set to True, the Telegram test environment will be used instead of the production environment
        use_file_db (``bool``, *optional*)
            use_file_db If set to True, information about downloaded and uploaded files will be saved between application restarts
        storage_optimizer (``bool``, *optional*)
            storage_optimizer If set to True, old files will automatically be deleted
        file_readable_names (``bool``, *optional*)
            file_readable_names If set to True, downloaded files will be saved under names as close as possible to the original name
            Otherwise, original file names will be ignored
        use_chat_db (``bool``, *optional*)
            use_chat_db If set to True, the library will maintain a cache of users, basic groups, supergroups, channels and secret chats
            Implies use_file_db
        use_message_db (``bool``, *optional*)
            use_message_db If set to True, the library will maintain a cache of chats and messages
            Implies use_chat_db

        allow_secret_chat (``bool``, *optional*)
            allow_secret_chat If set to True, support for secret chats will be enabled

        database_directory (``str``, *optional*)
            database_directory The path to the directory for the persistent database;
            if empty, the current working directory will be used
        files_directory (``str``, *optional*)
            files_directory The path to the directory for storing files;
            if empty, database_directory will be used
        work_dir (``str``, *optional*):
            work_dir The path to the directory for storing database and files;
            if database_directory or files_directory aren't defined this path will use
            if empty, a folder by profile name in the current working directory will be used
    """
    APP_VERSION = str(__version__)
    DEVICE_MODEL = '{} {}'.format(
        platform.python_implementation(),
        platform.python_version()
    )
    SYSTEM_VERSION = '{} {}'.format(
        platform.system(),
        platform.release()
    )
    LANG_CODE = 'en'
    TEST_MODE = False
    USE_FILE_DB = True
    STORAGE_OPTIMIZER = True
    FILE_READABLE_NAMES = True
    USE_CHAT_DB = True
    USE_MESSAGE_DB = True
    DATABASE_DIRECTORY = ''
    FILES_DIRECTORY = ''
    ALLOW_SECRET_CHAT = False
    WORK_DIR = '.'
    _section_name = 'tdlib'

    __slots__ = ['profile', 'test_mode', 'database_directory', 'files_directory', 'use_file_db', 'use_chat_db',
                 'use_message_db', 'allow_secret_chat', 'api_id', 'api_hash', 'lang_code', 'device_model',
                 'system_version', 'app_version', 'storage_optimizer', 'file_readable_names', 'work_dir']

    def __init__(self,
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
                 database_directory: str = None,
                 files_directory: str = None,
                 work_dir: str = '',
                 ):
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
        self.database_directory = database_directory
        self.files_directory = files_directory
        self.work_dir = work_dir

    def __getitem__(self, item):
        return getattr(self, item, None)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    @staticmethod
    def load_from_config(config, file_name: str, profile_name: str):

        parser = ConfigParser()

        def get_parser_method(param):
            """right get method for TDLib parameter"""
            if param == 'api_id':
                return parser.getint
            elif param in ['test_mode', 'use_file_db', 'storage_optimizer', 'file_readable_names', 'use_chat_db',
                           'use_message_db', 'allow_secret_chat']:
                return parser.getboolean
            else:
                return parser.get

        parser.read(file_name)

        if isinstance(config, TdlibParameters):
            section_name = config._section_name
        else:
            section_name = TdlibParameters._section_name

        has_section = parser.has_section(section_name)

        attrs = [a[0] for a in inspect.getmembers(TdlibParameters, lambda a: not (inspect.isroutine(a)))
                 if not a[0].startswith('_')] + ['API_ID', 'API_HASH']
        for attr in attrs:
            option = attr.lower()

            try:
                defined_value = config[option]
            except KeyError:
                defined_value = None

            if has_section:
                config_value = get_parser_method(option)(section_name, option, fallback=None)
            else:
                config_value = None

            if defined_value is None:
                if config_value is None:
                    config[option] = getattr(TdlibParameters, attr, None)
                    log.info('TDLib Parameter "%s" Not Defined, Using Default Value' % option)
                else:
                    config[option] = config_value
                    log.info('TDLib Parameter "%s" Not Defined, Using Config Value.' % option)
                continue

            if config_value is not None:
                log.info('Ignoring config value "%s"' % option)

        if not (config['api_id'] and config['api_hash']):
            raise AttributeError(
                'No API Key Found. '
                'More info: https://my.telegram.org'
            )

        if config['work_dir'] == TdlibParameters.WORK_DIR:
            new_dir = os.path.join(os.getcwd(), profile_name)
            config['work_dir'] = new_dir
            log.info('Work Directory Changed To %s' % new_dir)
