from .auth import Auth
from .proxy import Proxy
from .user import User
from .option import Option
from .log import Log


class Methods(
    Auth,
    Proxy,
    User,
    Option,
    Log
):
    pass
