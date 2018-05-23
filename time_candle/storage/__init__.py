"""This is the adapters package. It contains functions that appears to be useful
to remove, store, pull and add data to the DB.

"""


import app_logger


logger = app_logger.custom_logger('storage')


# Database will be represented as directories with multiple files, each file
# contains data for a specific object. Later it will be, maybe, divided by
# blocks of objects, not as separated files.

DB_ROOT = "db"
TASKS_ROOT = "tasks"
