from threading import Event
from pytdlib.api.errors import TLError


class Callback:
    def __init__(self, target: callable = lambda *args, **kwargs: None, args: list=None, kwargs: dict=None):
        self.target = target
        self.args = [] if args is None else args
        self.kwargs = {} if args is None else kwargs
        self.result = None
        self.event = Event()
        self.event.set()
        self.is_waited = False

    def run(self):
        if not self.is_waited:
            return self.target(*[self.result, *self.args], **self.kwargs)

    def wait(self, raise_error: bool=False, timeout: float=20):
        self.is_waited = True
        if self.event.is_set():
            if not self.result:
                self.event.clear()
                self.event.wait(timeout)

                if raise_error:
                    if not self.result:
                        raise TimeoutError
                    if isinstance(self.result, TLError):
                        raise self.result
            return self.result

    def __call__(self, *args, **kwargs):
        return self.run()
