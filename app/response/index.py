# -*- conding:utf-8 -*-
__author__ = "snake"

from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()

def _get_last_test_results():
    """1. 上次用例执行结果"""
    """
          "testreports": {
            "failed": {
                "count": 0,
                "data": []
            },
            "success": {
                "count": 2,
                "data": [
                    {
                        "cassid": 2,
                        "createtime": "2018-05-17 00:11:47",
                        "id": 31,
                        "result": "{\n  \"code\": 200, \n  \"data\": \"sjdh34gsalked23nlsakn45dudaj\", \n  \"msg\": \"登陆成功\"\n}\n",
                        "runtime": "0.011257",
                        "status": 0,
                        "validate": "r.status_code==200",
                        "version": 3
                    },
                    {
                        "cassid": 3,
                        "createtime": "2018-05-17 00:15:45",
                        "id": 32,
                        "result": "{\n  \"code\": 200, \n  \"msg\": \"操作成功\"\n}\n",
                        "runtime": "0.012227",
                        "status": 0,
                        "validate": "r.status_code==200",
                        "version": 3
                    }
                ]
            }
        }

    """

    # 获取上次执行的测试用例
    success_sql = "select * from t_reports where version in" \
                  " (select max(version) as version from t_reports) and status='成功'"
    failed_sql = "select * from t_reports where version in" \
                 " (select max(version) as version from t_reports) and status!='成功'"
    success_results = dbfucs.query(success_sql)
    failed_results = dbfucs.query(failed_sql)

    last_testreports = {}
    last_testreports["success"] = {"data": success_results, "count": len(success_results)}
    last_testreports["failed"] = {"data": failed_results, "count": len(failed_results)}

    return last_testreports


def _get_last_test_result_runtime():
    """2. 上次用例执行时间分段统计图"""
    """
        时间分段统计：
        极快: t<1s
        快速: 1s< t <3s
        慢: 3s < t < 5s
        超级慢: t>5s

        "runtimecount": {
            "fast": {
                "count": 0,
                "times": []
            },
            "faster": {
                "count": 2,
                "times": [
                    0.011257,
                    0.012227
                ]
            },
            "slow": {
                "count": 0,
                "times": []
            },
            "slowly": {
                "count": 0,
                "times": []
            }
        },
    """
    faster, fast, slow, slowly = {}, {}, {}, {}
    faster["count"], fast["count"], slow["count"], slowly["count"] = 0, 0, 0, 0
    faster["times"], fast["times"], slow["times"], slowly["times"], = [], [], [], []
    success_sql = "select * from t_reports where version in" \
                  " (select max(version) as version from t_reports) and status='成功'"
    failed_sql = "select * from t_reports where version in" \
                 " (select max(version) as version from t_reports) and status!='成功'"
    success_results = dbfucs.query(success_sql)
    failed_results = dbfucs.query(failed_sql)
    for result in (success_results, failed_results):
        for r in result:
            try:
                runtime = float(r.get("runtime"))
            except:
                runtime = 100.0
            if runtime < 1.0:
                faster["count"] += 1
                faster["times"].append(runtime)
            if runtime > 1.0 and runtime < 3.0:
                fast["count"] += 1
                fast["times"].append(runtime)
            if runtime > 3.0 and runtime < 5.0:
                slow["count"] += 1
                slow["times"].append(runtime)
            if runtime > 5.0:
                slowly["count"] += 1
                slowly["times"].append(runtime)

    return {"faster": faster, "fast": fast, "slow": slow, "slowly": slowly}


def _get_modules_count():
    """  3. 每个项目的模块统计 """
    """
        "modulescount": [
            {
                "count": 2,
                "modules": [
                    {
                        "createtime": "2018-05-17 21:47:48",
                        "explain": "WEB端测试模块1",
                        "id": 1,
                        "leader": "浪晋",
                        "modules": "WEB模块1",
                        "projectid": 1,
                        "remark": "备注",
                        "updatatime": "2018-05-17 21:47:48"
                    },
                    {
                        "createtime": "2018-05-17 21:47:52",
                        "explain": "WEB端测试模块2",
                        "id": 6,
                        "leader": "snake",
                        "modules": "WEB模块2",
                        "projectid": 1,
                        "remark": "备注",
                        "updatatime": "2018-05-17 21:47:52"
                    }
                ],
                "project": {
                    "createtime": "2018-05-17 21:48:25",
                    "explain": "WEB端",
                    "id": 1,
                    "leader": "浪晋",
                    "productid": 1,
                    "project": "WEB项目",
                    "remark": "备注",
                    "updatatime": "2018-05-17 21:48:25"
                }
            },
            {
                "count": 2,
                "modules": [
                    {
                        "createtime": "2018-05-17 21:47:52",
                        "explain": "APP端测试模块1",
                        "id": 7,
                        "leader": "snake",
                        "modules": "APP模块1",
                        "projectid": 6,
                        "remark": "备注",
                        "updatatime": "2018-05-17 21:47:52"
                    },
                    {
                        "createtime": "2018-05-17 21:47:52",
                        "explain": "APP端测试模块2",
                        "id": 8,
                        "leader": "snake",
                        "modules": "APP模块2",
                        "projectid": 6,
                        "remark": "备注",
                        "updatatime": "2018-05-17 21:47:52"
                    }
                ],
                "project": {
                    "createtime": "2018-05-17 21:48:21",
                    "explain": "APP端",
                    "id": 6,
                    "leader": "snake",
                    "productid": 1,
                    "project": "APP项目",
                    "remark": "备注",
                    "updatatime": "2018-05-17 21:48:21"
                }
            }
        ]
    """
    modulescount = []
    sql = "select projectid from t_modules GROUP BY projectid"
    for results in dbfucs.query(sql):
        singeitem = {}

        # 统计count和modules
        sql = "select * from t_modules where projectid = %d" % results.get("projectid")
        res = dbfucs.query(sql)
        if res:
            singeitem["count"] = len(res)# count
            singeitem["modules"] = res   # modules
            projectid = results.get("projectid")

            # 统计project
            sql = "select * from t_project where id = %d" % projectid
            res = dbfucs.query(sql)
            if res:
                singeitem["project"] = res[0]

            modulescount.append(singeitem)

    return modulescount


def _get_testcases_count():
    """4. 每个模块的用例统计"""
    testcasscount = []
    sql = "select moduleid from t_testcass GROUP BY moduleid"

    # 循环每一个module的id
    for id in dbfucs.query(sql):
        singeitem = {}

        # 统计count和testcases
        sql = "select * from t_testcass where moduleid = %d" % id.get("moduleid")
        res = dbfucs.query(sql)
        if res:
            singeitem["count"] = len(res)# count
            singeitem["testcases"] = res   # modules
            moduleid = id.get("moduleid")

            # 统计module
            sql = "select * from t_modules where id = %d" % moduleid
            res = dbfucs.query(sql)
            if res:
                singeitem["module"] = res[0]

            testcasscount.append(singeitem)

    return testcasscount


@bp.route("/index", methods=["get"])
def index():
    """
    后台首页统计图接口 - 单接口
    1. 上次用例执行成功/失败图
    2. 上次用例执行时间分段统计图
    3. 每个项目的模块统计
    4. 每个模块的用例统计
    :return:
    """
    response = {}
    response["modulescount"] = _get_modules_count()             # 项目中模块统计
    response["testcasscount"] = _get_testcases_count()          # 项目中模块统计
    response["testreports"] = _get_last_test_results()          # 上次用例
    response["runtimecount"] = _get_last_test_result_runtime()  # 上次执行时间分段统计

    return jsonify({"datas": response, "code": 200, "msg": "查询成功"})


@bp.route("/testcasscount", methods=["get"])
def testcasscount():
    """
    4. 每个模块的用例统计
    :return:
    """

    response = {}
    response["code"] = 200
    response["msg"] = "查询成功!"
    response["datas"] = _get_testcases_count()

    return jsonify(response)


@bp.route("/modulescount", methods=["get"])
def modulescount():
    """
    3. 每个项目的模块统计
    :return:
    """
    response = {}
    response["code"] = 200
    response["msg"] = "查询成功!"
    response["datas"] = _get_modules_count()

    return jsonify(response)


@bp.route("/runtimecount", methods=["get"])
def runtimecount():
    """
    2. 上次用例执行时间分段统计图
    :return:
    """
    response = {}
    response["code"] = 200
    response["msg"] = "查询成功!"
    response["datas"] = _get_last_test_result_runtime()

    return jsonify(response)


@bp.route("/testreportscount", methods=["get"])
def testreportscount():
    """
    1. 上次用例执行结果统计
    :return:
    """
    response = {}
    response["code"] = 200
    response["msg"] = "查询成功!"
    response["datas"] = _get_last_test_results()

    return jsonify(response)
