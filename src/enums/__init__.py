from collections import namedtuple as struct
from enum import Enum, unique


"""This is the primary enumerations used in the time-candle application and this
is the first test documentation. 
  TODO: something useful in this life

"""

__all__ = []

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)
