from logging import NOTSET, Handler


class ListLogHandler(Handler):

    def __init__(self, level=NOTSET):
        super().__init__(level)
        self._messages = []

    def emit(self, record):
        msg = self.format(record)
        self._messages.append(msg)

    @property
    def messages(self):
        return self._messages


