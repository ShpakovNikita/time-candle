"""This is the adapters package. It contains functions that appears to be useful
to remove, store, pull and add data to the DB.
  TODO: something useful in this life

"""


import pkgutil
import inspect
import app_logger
import os

__all__ = []
logger = app_logger.custom_logger('storage')


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
