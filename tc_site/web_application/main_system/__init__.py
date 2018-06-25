import time_candle.app_logger
from main_system import config
import os


if not os.path.exists(config.BASE_DIR):
    os.makedirs(config.BASE_DIR)

time_candle.app_logger.setup_logging(
    enabled=config.ENABLED,
    log_conf=config.LOG_CONF_PATH,
    log_path=config.LOG_PATH,
    time_format=config.TIME_FORMAT
)


logger = time_candle.app_logger.custom_logger('web_app_system')
