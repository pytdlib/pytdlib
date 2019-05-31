from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class SignIn(BaseTelegram):

    def sign_in(self, code: str = None, password: str = None):
        if code:
            req = functions.CheckAuthenticationCode(code, "", "")
        else:
            req = functions.CheckAuthenticationPassword(password)
        return self.send(req)
