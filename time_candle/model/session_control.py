import sys
from time_candle.exceptions import custom_excepthook


def start_session(dev_opt='dev'):
    if dev_opt == 'dev':
        pass
    elif dev_opt == 'user':
        sys.excepthook = custom_excepthook
    else:
        raise ValueError('session option is wrong!')
