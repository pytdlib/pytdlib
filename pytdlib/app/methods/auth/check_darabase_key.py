from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class CheckDatabaseKey(BaseTelegram):

    def check_db_key(self, key: str):
        return self.send(functions.CheckDatabaseEncryptionKey(encryption_key=key))
