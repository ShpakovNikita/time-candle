import enums


class Priority(enums.Enum):

    MIN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    MAX = 4

    _current = MAX

    # Maybe there is no need in this property.
    # Then TODO: add @enums.unique
    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        if value <= self.MIN or value > self.MAX:
            raise ValueError("Value is invalid")
        self._current = value
