from pytdlib.api import functions
from ...ext import BaseTelegram


class SignIn(BaseTelegram):

    def sign_in(self, code: str = None, password: str = None):
        if code:
            req = functions.CheckAuthenticationCode(code, "", "")
        else:
            req = functions.CheckAuthenticationPassword(password)
        return self.send(req)
