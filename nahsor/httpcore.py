# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：封装了requests的方法
'''
import requests
from logger import Logger
from exception import NotFoundMethodError
requests.packages.urllib3.disable_warnings()
logger = Logger()


METHODS = ['GET', 'POST', 'HEAD', 'TRACE', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']


class HTTPClient(object):
    """
    http请求的client。初始化时传入url、method等。
    HTTPClient('http://www.baidu.com').send()
    <Response [200]>
    """
    def __init__(self, url, method='GET', **kwargs):
        self.url = url
        self.session = requests.session()
        self.method = method.upper()
        if self.method not in METHODS:
            raise NotFoundMethodError('不支持的method:{0}，请检查传入参数！'.format(self.method))


    def send(self,**kwargs):
        try:
            response = self.session.request(method=self.method, url=self.url, **kwargs)
            response.encoding = 'utf-8'
            return response
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as timeout:
            logger.error("接口连接超时", timeout)
            raise
