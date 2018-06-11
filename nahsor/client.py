# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：启动接口测试的入口
'''
import unittest
from httpcore import httptest
from respones import resobj
from testcase import import_json_file, chick_type_json
from validate import chick_validate
from logger import Logger

logger = Logger()

def run():
    '''
    ?
    '''
    filename = "test_json.json"
    filename = import_json_file(filename)
    json_context = chick_type_json(filename)
    request = json_context.get("request")
    validates = json_context.get("validates")
    try:
        response = httptest(request)
        validatelist = resobj(response, validates)
        chick_validate(validatelist)
    except:
        logger.error("EEEEEEEE")


run()

