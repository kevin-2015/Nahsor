# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：封装了requests的方法
'''
import requests
from logger import Logger
Logger = Logger()


def run_http_test(testname, request):
    '''
    对HTTP接口发送请求
    '''
    Logger.info("开始执行测试用例[%s]" % testname)
    Logger.info("接口请求地址为 --> %s" % request["url"])
    Logger.info("接口请求方法为 --> %s" % request["method"])
    Logger.info("接口请求header --> %s" % request["headers"])
    Logger.info("接口请求数据为 --> %s" % request["json"])
    try:
        r = requests.request(**request)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as timeout:
        Logger.error("测试用例[%s]在执行过程中出现异常，错误信息为 --> %s" % (testname, timeout))
    Logger.info("接口响应时间为 --> %ss" % r.elapsed.total_seconds())
    Logger.info("接口响应状态为 --> %s" % r.status_code)
    Logger.info("接口响应内容为 --> %s" % r.text)
    if r.status_code == 200:
        return r
    else:
        # Logger.error("测试用例[%s]在执行过程中出现异常，错误信息为 --> [code:%s],[error:%s]" % (testname, r.status_code, r.text))
        raise Exception()

