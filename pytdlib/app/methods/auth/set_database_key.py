from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions


class SetDatabaseKey(BaseTelegram):

    def set_db_key(self, key: str):
        return self.send(functions.SetDatabaseEncryptionKey(new_encryption_key=key))
