# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：日志类
'''
import logging
import coloredlogs


class Logger:
    def __init__(self,username='LangJin', level='DEBUG'):
        self.logger = logging.getLogger(username)
        coloredlogs.install(level)

    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warn(self,message):
        self.logger.warn(message)

    def error(self,message):
        self.logger.error(message)

    def critical(self,message):
        self.logger.critical(message)


if __name__ =='__main__':
    logger = Logger()
    logger.debug("this is a debugging message")
    logger.info("this is an informational message")
    logger.warn("this is a warning message")
    logger.error("this is an error message")
    logger.critical("this is a critical message")
