from cleo import Command

from ..handlers import FolderWatcher


class WatchCommand(Command):
    """
    Watch a folder

    watch
        {folder : Which folder do you want to watch?}
        {command? : What command to run?}
        {--d|debug : Debug mode?}
        {--k|kind=any : Whether to watch for folders or files? allowed: any,files,folders}
        {--i|interval=2 : How long to wait after an event for another one?}
        {--e|event=* : What file system even to watch for? allowed: any,create,delete,modified,moved}
    """

    ALLOWED_KIND = ["any", "folders", "files"]
    ALLOWED_EVENTS = ["any", "create", "delete", "modify", "move"]

    def handle(self):
        folder = self.argument("folder")
        command = self.argument("command")

        event = self.option("event")
        kind = self.option("kind")
        interval = self.option("interval")
        debug = self.option("debug")

        try:
            interval = int(interval)
        except Exception:
            raise Exception("Interval cannot be converted to int, interval must be an integer")

        if kind not in self.ALLOWED_KIND:
            raise Exception("Kind must be one of 'any', 'folders' or 'files'. Default is 'any'")

        if "any" in event or len(event) < 1:
            event = ["any"]
        elif not all(one_event in self.ALLOWED_EVENTS for one_event in event):
            raise Exception("Invalid event, allowed events are", ",".join(self.ALLOWED_EVENTS))

        if debug:
            print("folder", folder)
            print("command", command)
            print("event", event)
            print("kind", kind)
            print("interval", interval)
        else:
            if command:
                watcher = FolderWatcher(folder, command, interval=interval, kind=kind, event=event)
            else:
                watcher = FolderWatcher(folder, interval=interval, kind=kind, event=event)

            self.line(
                f"Watching folder: {folder} for {event} events in {kind} with interval {interval}s and running command: {command}"
            )
            watcher.run()
