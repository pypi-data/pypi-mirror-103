import logging
import shlex
import time
from datetime import datetime, timedelta
from subprocess import run
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)


class MyHandler(FileSystemEventHandler):
    def __init__(self, folder, command_to_run, interval, kind, event):
        self._folder = folder
        self._command = command_to_run
        self._interval = interval
        self._kind = kind
        self._last_modified = datetime.now()
        self._event = event

    def should_process_event(self, event):
        process = False

        if self._kind == "any":
            process = True
        elif event.is_directory and self._kind == "folders":
            process = True
        elif self._kind == "files" and not event.is_directory:
            process = True

        return process

    def process_event(self, event):
        if self.should_process_event(event):
            if self._interval and (datetime.now() - self._last_modified) < timedelta(seconds=self._interval):
                print("skip this event, interval:", self._interval)
                return
            else:
                self._last_modified = datetime.now()
            print(f"Event type: {event.event_type}  path : {event.src_path}")
            if self._command:
                try:
                    run(shlex.split(self._command), shell=True, check=True)
                except Exception:
                    raise

    def on_created(self, event):
        if "any" in self._event or "create" in self._event:
            self.process_event(event)

    def on_deleted(self, event):
        if "any" in self._event or "delete" in self._event:
            self.process_event(event)

    def on_modified(self, event):
        if "any" in self._event or "modify" in self._event:
            self.process_event(event)

    def on_moved(self, event):
        if "any" in self._event or "move" in self._event:
            self.process_event(event)


class FolderWatcher:
    """The class which abstracts the watching and handling of file system events

    :param src_path: The folder to watch
    :type src_path: string
    :param command_to_run: the command to run when a file modification is detected
    :type command_to_run: string
    """

    DEFAULT_INTERVAL = 2

    def __init__(self, src_path, command_to_run=None, interval=None, kind="any", event=["any"]):
        self.__src_path = src_path
        if isinstance(interval, (int)):
            self._interval = interval
        else:
            self._interval = self.DEFAULT_INTERVAL
        self.__event_handler = MyHandler(src_path, command_to_run, self._interval, kind, event)
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(self.__event_handler, self.__src_path, recursive=True)
