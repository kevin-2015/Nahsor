# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：封装了requests的方法
'''
import requests
# from logger import Logger
# from exception import NotFoundMethodError
requests.packages.urllib3.disable_warnings()
# logger = Logger()

def httptest(request):
    '''
    "request": {
        "url": "http://127.0.0.1/test",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "json": {
            "username": "admin",
            "password":"123456"
        }
    '''
    
    url = request.pop("url")
    method = request.pop("method")
    kwargs = request
    print(kwargs)
    response = requests.request(method,url,**kwargs)
    return response