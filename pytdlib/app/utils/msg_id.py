from threading import Lock
from time import time


class MsgId:
    last_time = 0
    offset = 0
    lock = Lock()

    def __new__(cls) -> int:
        with cls.lock:
            now = time()
            cls.offset = cls.offset + 4 if now == cls.last_time else 0
            msg_id = int(now * 2 ** 32) + cls.offset
            cls.last_time = now

            return msg_id
