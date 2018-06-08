# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：启动接口测试的入口
'''

filename = import_json_file(filename)
json_context = chick_type_json(filename)
request = json_context.get("request")
validates = json_context.get("validates")
response = httptest(request)
validatelist = resobj(response, validates)
chick_validate(validatelist)
