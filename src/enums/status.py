from src import enums


class Status(enums.Enum):

    EXPIRED = 0
    CANCELLED = 1
    IN_PROGRESS = 2
    DONE = 3

    _current = IN_PROGRESS

    # Maybe there is no need in this property.
    # Then TODO: add @enums.unique
    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        if value <= self.EXPIRED or value > self.DONE:
            raise ValueError("Value is invalid")
        self._current = value
