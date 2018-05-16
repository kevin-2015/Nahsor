# -*- coding:utf-8 -*-
import json
from app.core.runner import Runner
from app.utils.log import Logger

def jsonfile(filename):
    '''
    判断导入的json文件格式是否合法
    '''
    filetype = filename.split(".")
    # print(filetype[-1])
    if filetype[-1] == "json" and filename.startswith("test"):
        return filename
    else:
        Logger().error("导入的JSON文件格式不正确，请检查JSON格式！")
        return None



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

