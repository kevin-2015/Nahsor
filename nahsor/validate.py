# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：对预期结果和实际结果做校验
'''



def chick_validate(validatelist):
    '''
    validatelist = ["a=1","b=2"]
    '''
    for validate in validatelist:
        assert eval(validate)