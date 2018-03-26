from datetime import datetime, date, time


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
