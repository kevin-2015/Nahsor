# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：解析json为用例的各种方法
'''
import json
from logger import Logger
logger = Logger()


def import_json_file(filename):
    '''
    filename = "test_*.json"
    说明：判断导入的json文件名/格式是否合法
    '''
    filetype = filename.split(".")
    if filetype[-1] == "json" and filename.startswith("test"):
        return filename
    else:
        logger.error("导入的JSON文件格式不正确，请检查JSON格式！")
        exit()


def chick_type_json(filename):
    '''
    检查json文件的内容
    "testcase": {
        "name": "teatname",
        "request": {
            "url": "/api/get-token",
            "method": "POST",
            "headers": {
                "app_version": "$app_version"
            },
            "json": {
                "username": "admin","password":"123456"
            },
            "extract": [
                {"token": "content.token"}
            ],
            "validate": [
                {"eq": ["status_code", 200]},
                {"eq": ["headers.Content-Type", "application/json"]},
                {"eq": ["content.success", true]}
            ]
        }
    }
    '''
    with open(filename, 'r') as f:
        json_context = json.load(f)
        # print(all_tests)
    if not isinstance(json_context, list):
        raise
    for testcass in json_context:
        if not testcass:
            logger.error("没有发现测试用例，结束用例执行！")
    if testcass.get("testcase"):




def collect_file_cass(filename):
    '''
    读取json并执行用例。
    '''
    with open(filename, 'r') as f:
        all_tests = json.load(f)
        # print(all_tests)
    for test in all_tests:
        if not test:
            Logger().error("没有发现测试用例，结束用例执行！")
        # try:
        runner = Runner(test)
        yield runner.run_test()
        # except:
        #     print("【%s】用例执行失败" % test["cass_name"])


def get_reports_max_version():
    """
    获取测试报告的最后一个版本
    :return:
    """
    from app.utils.dbfucs import query
    sql = "select max(version) as version from t_reports"
    r = query(sql)[0]
    if r.get("version"):
        return r.get("version") + 1
    else:
        return 1


def collect_db_cass(jsoncasss):
    '''
    读取json并执行用例。
    '''
    # 获取当前用例测试结果的最大版本号
    version = get_reports_max_version()
    for test in jsoncasss:
        if not test:
            Logger().error("没有发现测试用例，结束用例执行！")
        try:
            runner = Runner(test)
            yield runner.run_test(version)
        except Exception as e:
            Logger().error("测试用例[%s]执行失败，失败原因 --> %s"  % (test["testname"], e))


def get_global_values(request):
    '''
    替换request里带了$的参数为全局变量中的值。
    {
        "url": "http://127.0.0.1:2333/test",
        "json": {'token': '$token'},
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "timeout": 10
    }
    '''
    execlist = []
    for key in request:
        if type(request[key]) == dict:
            for key1 in request[key]:
                # print(key)
                if '$' == request[key][key1][:1]:
                    # print(key1)
                    execkey = "request['%s']['%s'] = extracts['%s']" % (key, key1, request[key][key1][1:])
                    execlist.append(execkey)
                    # print(execkey)
    return execlist


def extract_global_values(extract):
    '''
    [
        {"token":"r.json()["data"]"},
        {"token":"r.json()["data"]"}
    ]
    '''
    execlist = []
    for extdict in extract:
        key = list(extdict.keys())[0]
        value = extdict[key]
        extfuc = "extracts['%s'] = %s" % (key, value)
        execlist.append(extfuc)
    return execlist


def run_execs_test(execlist):
    '''
    执行赋值类型的表达式
    extracts['token'] = 'ssdsfsdf4s6f54s6f1a3s'
    '''
    # print(**arg)
    if len(execlist) != 0:
        for execkey in execlist:
            print(execkey)
            exec(execkey)


def run_evals_test(evalist):
    '''
    执行判断类型的表达式
    "12233" == 'sdsdd'
    '''
    if len(evalist) != 0:
        for evalkey in evalist:
            print(evalkey)
            eval(evalkey)


def run_validata_test(testname, validatelist):
    '''
    测试用例的检查点执行
    '''
    if len(validatelist) != 0:
        for validatekey in validatelist:
            res = eval(validatekey)
            if res == True:
                Logger.info("测试用例[%s]检查点执行成功,检查点信息为 --> %s" % (testname, validatekey))
            else:
                Logger.war("测试用例[%s]检查点执行失败,检查点信息为 --> %s" % (testname, validatekey))


def get_validata_test(validates):
    '''
    提取的校验方法
    arg : [{"Equal": ["r.status_code", "200"]}]
    '''
    asserts = {
        "Equal": "==",
        "NotEqual": "!=",
        "True": "is True",
        "False": "is False",
        "Is": "is",
        "IsNot": "is not",
        "IsNone": "is None",
        "IsNotNone": "is not None",
        "In": "in",
        "NotIn": "not in",
        "IsInstance": "isinstance",
        "NotIsInstance": "not isinstance"
    }
    validatelist = []
    for validate in validates:
        key = list(validate.keys())[0]
        # print(key)
        asserts[key]
        validate[key]
        validatekey = validate[key][0] + asserts[key] + validate[key][1]
        validatelist.append(validatekey)

    return validatelist