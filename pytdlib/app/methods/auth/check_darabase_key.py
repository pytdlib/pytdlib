from pytdlib.api import functions
from ...ext import BaseTelegram


class CheckDatabaseKey(BaseTelegram):

    def check_db_key(self, key: str):
        return self.send(functions.CheckDatabaseEncryptionKey(encryption_key=key))
