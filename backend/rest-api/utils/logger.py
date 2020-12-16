from loguru import logger
from utils.patterns import Singleton

class Logger():
    @staticmethod
    def log(message: str):
        logger.debug(message)