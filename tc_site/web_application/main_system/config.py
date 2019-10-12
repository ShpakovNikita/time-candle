"""This is the config file for web interface"""
import os


DEPLOY = False

if not DEPLOY:
    BASE_DIR = os.path.join(os.environ['HOME'], 'appdata/web')
else:
    BASE_DIR = '.'


# This is the log file name
LOG_FILE = 'config.log'
LOG_PATH = os.path.join(BASE_DIR, LOG_FILE)
LOG_CONF = 'logging.conf'
LOG_CONF_PATH = os.path.join(BASE_DIR, LOG_CONF)

# For logging formatting
TIME_FORMAT = '%d/%b/%Y %H:%M:%S'

# This is lib database file name (but we will be using postgresql)
DATABASE_FILE = 'data.db'
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_FILE)

# If None then db from URL will be loaded
DATABASE_CONFIG = None

DATABASE_URL = 'postgres://hicxmadptdigzw:c700b29bc7775f349fa9d1246847a874905f9fbd0a2976c508c211987d2739ae@ec2-54-228-181-43.eu-west-1.compute.amazonaws.com:5432/ddeov1tnkuco57'

# This is the logging flag
ENABLED = True

if not DEPLOY:
    from .local import *
