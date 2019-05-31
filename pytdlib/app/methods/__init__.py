from .auth import Auth
from .proxy import Proxy
from .user import User


class Methods(
    Auth,
    Proxy,
    User
):
    pass
