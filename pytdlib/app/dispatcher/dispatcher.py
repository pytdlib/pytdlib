import logging
from collections import OrderedDict
from queue import Queue
from threading import Thread

from ..events import Update

log = logging.getLogger(__name__)


class Dispatcher:

    def __init__(self, client, workers: int):
        self._client = client
        self._workers = workers
        self._workers_list = []
        self.events_queue = Queue()
        self.event_parsers = {}
        self.events = {}
        self.default_event_id = Update.EVENTS[0]

    def start(self):
        for i in range(self._workers):
            self._workers_list.append(
                Thread(
                    target=self.event_worker,
                    name="EventWorker#{}".format(i + 1)
                )
            )

            self._workers_list[-1].start()

    def stop(self):
        for _ in range(self._workers):
            self.events_queue.put(None)

        for worker in self._workers_list:
            worker.join()

        self._workers_list.clear()

    def add_event(self, event: Update):
        for event_name in event.EVENTS:
            if event_name not in self.event_parsers:
                self.event_parsers[event_name] = event.parser
                self.events[event_name] = OrderedDict([(event.group, [])])
            elif event.group not in self.events[event_name]:
                self.events[event_name][event.group] = []
                self.events[event_name] = OrderedDict(sorted(self.events[event_name].items()))

            self.events[event_name][event.group].append(event)

    def remove_event(self, event: Update):
        for event_name in event.EVENTS:
            if event_name not in self.events:
                raise ValueError("Event {} does not exist. Event handler was not removed.".format(event_name))
            if event.group not in self.events[event_name]:
                raise ValueError("Group {} does not exist. Event handler was not removed.".format(event.group))

            self.events[event_name][event.group].remove(event)
            if not self.events[event_name][event.group]:
                del self.events[event_name][event.group]
            if not self.events[event_name]:
                del self.events[event_name]
                del self.event_parsers[event_name]

    def event_worker(self):

        while True:
            event = self.events_queue.get()

            if event is None:
                break

            event_id = event.ID if event.ID in self.event_parsers else self.default_event_id

            event_parser = self.event_parsers.get(event_id)

            if event_parser is None:
                continue

            parsed_event = event_parser(event)

            try:
                for event_group in self.events.get(event_id, {}).values():
                    for event_handler in event_group:
                        if event_handler.check(parsed_event):
                            try:
                                event_handler.callback(self._client, parsed_event)
                            except:
                                pass
                            break
            except:
                pass
