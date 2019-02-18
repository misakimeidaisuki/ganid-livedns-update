import os
import logging

class updateLog(object):
    def __init__(self, filename="update.log", level=logging.DEBUG):
        self.__path = os.path.dirname(os.path.realpath(__file__))

        self.logger = logging.getLogger()
        self.logger.setLevel(level)

        format = "%(asctime)s - [%(levelname)s]:%(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(format, datefmt=date_format)

        filepath = os.path.join(self.__path, filename)
        file_handler = logging.FileHandler(filepath);
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)
    def info(self, message):
        self.logger.info(message)
    def warning(self, message):
        self.logger.warning(message)

    def setLevel(self, level):
        self.logger.setLevel(level)
