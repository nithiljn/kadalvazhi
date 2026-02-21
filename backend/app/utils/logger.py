import logging
import sys
from pathlib import Path
from typing import Optional
from app.config import settings


#LOG FILE PATHs
LOG_DIR = Path(__file__).parent.parent.parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)
APP_LOG_FILE = LOG_DIR / 'app.log'
ERROR_LOG_FILE = LOG_DIR / 'error.log'

# LOG FORMAT
# HOW LOGS WILL LOOK:
# 2025-02-12 14:30:45,123 - app.services.weather_service - INFO - Fetching weather
# ↑ Timestamp              ↑ File that logged            ↑ Level  ↑ Message
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
def get_log_level()->int:
    """Get log level based on settings.DEBUG"""
    if settings.debug:
        return logging.DEBUG
    return logging.INFO

#CREATE FORMATTERS
# FORMATTER: How to format log messages
# WHY: Separate formatter creation = reusable for different handlers
formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT,
            )
def get_handler()->list[logging.Handler]:
    """ 
    HANDLERS = Where logs go (console, file, database, etc.)
    WE CREATE 3 HANDLERS:
    1. Console (terminal output) - for development
    2. File (app.log) - all logs
    3. File (error.log) - only errors
    """
    handlers =[]

    #terminal handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(get_log_level())# DEBUG in dev, INFO in prod
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    #file handler
    # CONTAINS: All levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    file_handler = logging.FileHandler(
                   APP_LOG_FILE,
                   mode='a' , #WHY 'a': Append (don't delete old logs)
                   encoding='utf-8'  # WHY: Support Tamil characters (கடல்வழி)
                   )
    file_handler.setLevel(get_log_level())
    file_handler.setFormatter(formatter)
    handlers.append(file_handler)

    #error handler
    error_handler = logging.FileHandler(
                    ERROR_LOG_FILE,
                    mode='a',
                    encoding='utf-8',
                    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    handlers.append(error_handler)

    return handlers

# GET LOGGER FUNCTION (MAIN FUNCTION)
def get_logger(name:Optional[str]=None)->logging.Logger:
    """Get logger for the application"""
    #If logger with this name exists, return it (cached)
    # If not, create new one
    logger = logging.getLogger(name)
    logger.setLevel(get_log_level())
    if not logger.handlers:
        for handler in get_handler():
            logger.addHandler(handler)
    logger.propagate = False #WHY: Prevents logs from appearing twice
    return logger

logger = get_logger(__name__)

logger.info("Logger initialized")