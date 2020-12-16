from loguru import logger
from utils.patterns import SingletonMeta

class Logger():
    @staticmethod
    def log(self, message: str):
        logger.debug(message)