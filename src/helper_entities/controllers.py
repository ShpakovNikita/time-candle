from datetime import datetime, date, time
import helper_entities as package


def _check_int_field(value):
    if isinstance(value, int):
        return value
    if not isinstance(value, float):
        try:
            value = value.__int__()
        except AttributeError:
            pass
        else:
            if isinstance(value, int):
                return value
            raise TypeError('__int__ returned non-int (type %s)' %
                            type(value).__name__)
        raise TypeError('an integer is required (got type %s)' %
                        type(value).__name__)
    raise TypeError('integer argument expected, got float')


class BehaviorController:
    def __init__(self,
                 year=datetime.today().year,
                 month=datetime.today().month,
                 day=datetime.today().day,
                 hour=datetime.today().hour,
                 minute=datetime.today().minute):

        # Here is the datetime class already checking the validation of the
        # fields in the __new__() method
        self._creation_time = datetime(year,
                                       month=month,
                                       day=day,
                                       hour=hour,
                                       minute=minute)
        self._set_of_rules = []


class DeadlineController(BehaviorController):
    def __init__(self,
                 year=datetime.today().year,
                 month=datetime.today().month,
                 day=-1,
                 hour=-1,
                 minute=-1):
        super(self, DeadlineController).__init__()
        self._set_of_rules = None
        self._deadline_time = datetime(year,
                                       month=month,
                                       day=day,
                                       hour=hour,
                                       minute=minute)
        self._interval_time = None

    @classmethod
    def make_deadline_controller(cls,
                                 deadline_time=datetime.today(),
                                 interval_time=datetime(year=package.predefined_time.year,
                                                        month=package.predefined_time.month,
                                                        day=7)):
        obj = cls(deadline_time.year,
                  deadline_time.month,
                  deadline_time.day,
                  deadline_time.hour,
                  deadline_time.minute)

        obj.interval_time = interval_time
        obj.interval_time.year = 0
        return obj

    @property
    def interval_time(self):
        return self._interval_time

    @interval_time.setter
    def interval_time(self, value):
        # This is a dumb check, because it is too close to the impossible state
        # to be true
        if value.year - package.predefined_time.year >= 1:
            raise ValueError("interval_time year value is invalid")
        self._interval_time = value


