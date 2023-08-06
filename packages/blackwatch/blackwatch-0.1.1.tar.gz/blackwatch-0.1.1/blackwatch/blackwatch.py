import logging
from cleo import Application

from blackwatch.commands import WatchCommand


logger = logging.getLogger(__name__)
console = logging.StreamHandler()
logger.addHandler(console)


class BlackWatchApplication(Application):
    _version = "0.1.0"


application = BlackWatchApplication()
application.add(WatchCommand())
