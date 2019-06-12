from threading import Event


class Result:
    def __init__(self):
        self.value = None
        self.event = Event()
