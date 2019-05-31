class Update:
    EVENTS = ["AllEvents"]

    def __init__(self, filters=None, group: int = 0, events: set = EVENTS, callback: callable = None):
        self.EVENTS = events
        self.filters = filters
        self.group = group
        self.callback = callback

    def check(self, update):
        return (
            self.filters(update)
            if callable(self.filters)
            else True
        )

    @classmethod
    def parser(cls, event):
        return event
