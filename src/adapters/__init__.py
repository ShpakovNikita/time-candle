"""This is the adapters package. It contains functions that appears to be useful
to remove, store, pull and add data to the DB.
  TODO: something useful in this life

"""


import pkgutil
import inspect
import os

__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)


# Database will be represented as directories with multiple files, each file
# contains data for a specific object. Later it will be, maybe, divided by
# blocks of objects, not as separated files.

DB_ROOT = "db"
TASKS_ROOT = "tasks"


def check_for_database(directory, file=None):
    if not os.path.exists(directory):
        os.makedirs(directory)
    if file is not None:
        out_val = open(directory + "/" + file, 'w+')

    return out_val
