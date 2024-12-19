'''Just a logger module'''

import os
import logging
from .config import LOG_LEVEL, LOG_DIR


class Logger:
    '''
    Centralized event logging utility

    :ivar name: Logger name for class or module
    :type name: str
    '''

    def __init__(self, name: str):
        '''
        Logger initialization

        :param name: Logger name for class or module
        :type name: str
        '''
        self.logger = logging.getLogger(name)
        self.logger.setLevel(LOG_LEVEL)

        # Logging format
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

        # File handler
        log_file = os.path.join(LOG_DIR, "logs.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_format)
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        '''
        Log message as debug

        :param message: Message to log
        :type message: str
        '''
        self.logger.debug(message)

    def info(self, message: str):
        '''
        Log message as info

        :param message: Message to log
        :type message: str
        '''
        self.logger.info(message)

    def warning(self, message: str):
        '''
        Log message as warning

        :param message: Message to log
        :type message: str
        '''
        self.logger.warning(message)

    def error(self, message: str):
        '''
        Log message as error

        :param message: Message to log
        :type message: str
        '''
        self.logger.error(message)

    def critical(self, message: str):
        '''
        Log message as critical

        :param message: Message to log
        :type message: str
        '''
        self.logger.critical(message)


if __name__ == "__main__":
    log = Logger("logger")

    log.debug("Debug message")
    log.error("Error message")
    log.info("Info message")
    log.warning("Warning message")
    log.critical("Critical message")
