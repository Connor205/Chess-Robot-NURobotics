import threading
from loggingConstants import formatter, handler
import logging


class ThreadWithReturn:

    def __init__(self, function, *args) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        self.function = function
        self.args = args
        self.result = None
        self.logger.info(
            f"Created ThreadWithReturn for function: {function.__name__}")

    def start(self):
        self.logger.info("Started ThreadWithReturn")
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        self.result = self.function(*self.args)
        self.logger.info("Finished running function in external thread")

    def getResult(self):
        return self.result

    def getActive(self):
        return self.thread.is_alive()
