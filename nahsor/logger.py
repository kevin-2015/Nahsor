# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：日志类
'''
import logging
import coloredlogs
logger = logging.getLogger('your-module')


coloredlogs.install(level='DEBUG')

# Some examples.
logger.debug("this is a debugging message")
logger.info("this is an informational message")
logger.warn("this is a warning message")
logger.error("this is an error message")
logger.critical("this is a critical message")