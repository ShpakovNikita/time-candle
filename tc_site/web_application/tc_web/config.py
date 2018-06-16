"""This is the config file for the command line interface"""
import os
import platform


if platform.system() == 'Linux':
    BASE_DIR = os.path.join(os.environ['HOME'], 'appdata/web')
else:
    BASE_DIR = 'appdata/web'

# This is the mode for out session. It can be user or dev. Depends on library
# stacktrace
VERBOSE = True

# This is the log file name
LOG_FILE = 'config.log'
LOG_PATH = os.path.join(BASE_DIR, LOG_FILE)
LOG_CONF = 'logging.conf'
LOG_CONF_PATH = os.path.join(BASE_DIR, LOG_CONF)

# This is lib database file name (but we will be using postgresql)
DATABASE_FILE = 'data.db'
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_FILE)

DATABASE_CONFIG = {
            'NAME': 'mydb',
            'USER': 'shaft',
            'HOST': '/var/run/postgresql',
            'PASSWORD': '',
            'PORT': '5432'}

# This is the user (cli) database file name
USERS_DATABASE_FILE = 'users.db'
USERS_DATABASE_PATH = os.path.join(BASE_DIR, USERS_DATABASE_FILE)

# This is the logging flag
ENABLED = True
