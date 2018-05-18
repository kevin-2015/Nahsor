# -*- conding:utf-8 -*-
__author__ = "snake"

from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


@bp.route("/getreports", methods=['post'])
def getreports():
    """
    获取根据版本获取用例执行结果
    {"version":""}：默认最大
    {"version":5}：版本为5的报告
    :return:
    """
    dictdata = request.get_json()
    if dictdata is None or dictdata.get("version") is None or dictdata.get("version") == "":
        sql = "SELECT * FROM t_reports \
                WHERE version = (SELECT max(version) FROM t_reports)"
    else:
        sql = "SELECT * FROM t_reports \
                WHERE version = %d" % dictdata.get("version")

    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/getversions", methods=['get'])
def getversions():
    """
    获取所有用例执行版本
    :return:
    """
    sql = "select version from t_reports group by version"
    versions = []
    for res in dbfucs.query(sql):
        versions.append(res.get("version"))
    response = {}
    response["code"] = 200
    response["data"] = {"versions":versions}
    response["msg"] = "查询成功！！！"
    return jsonify(response)


"""
    1. 条件查询
    1. 版本作为基础
    2. 可以进行产品、项目、模块来进行筛选
    3. 涉及到饼图、柱状图、记录

"""


def _get_test_results_by_conditions(**kwargs):
    """1. 根据条件获得用例执行结果
        :arg   参数可以传任意值
        {} / {"version": 14} / {"version": 14, "productid": 1}
        {"version": 14, "productid": 1, "projectid": 1} / {"version": 14, "productid": 1, "projectid": 1, "moduleid": 6}
    : return :
    """
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

    version = kwargs.get("version")
    productid = kwargs.get("productid")
    projectid = kwargs.get("projectid")
    moduleid = kwargs.get("moduleid")
    # 构造sql
    product_sql, project_sql, module_sql = ["", ""], ["", ""], ["", ""]
    if productid is not None and productid != "":
        product_sql.clear()
        product_sql.append(" ,t_product AS b")
        product_sql.append(" AND b.id=%d" % productid)
    if projectid is not None and projectid != "":
        project_sql.clear()
        project_sql.append(" ,t_project AS c")
        project_sql.append(" AND c.id=%d" % projectid)
    if moduleid is not None and moduleid != "":
        module_sql.clear()
        module_sql.append(" ,t_modules AS d")
        module_sql.append(" AND d.id=%d  AND e.moduleid = d.id" % moduleid)
    if version is not None and version != "":
        version_sql = "a.version = %d" % version
    else:
        version_sql = " version in (select max(version) as version from t_reports)"

    success_sql = "SELECT a.* FROM t_reports AS a %s %s  %s ,t_testcass as e WHERE %s AND a.`status`='成功' %s %s %s" \
                  " AND a.cassid = e.id" % (product_sql[0], project_sql[0], module_sql[0], version_sql, product_sql[1], project_sql[1], module_sql[1])

    failed_sql = "SELECT a.* FROM t_reports AS a %s %s  %s ,t_testcass as e WHERE %s AND a.`status`!='成功' %s %s %s" \
                  " AND a.cassid = e.id" % (product_sql[0], project_sql[0], module_sql[0], version_sql, product_sql[1], project_sql[1], module_sql[1])

    success_results = dbfucs.query(success_sql)
    failed_results = dbfucs.query(failed_sql)

    last_testreports = {}
    last_testreports["success"] = {"data": success_results, "count": len(success_results)}
    last_testreports["failed"] = {"data": failed_results, "count": len(failed_results)}

    return last_testreports


# 该做这里的条件统计了
def _get_test_result_runtime_by_conditions(**kwargs):
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
                  " (select max(version) as version from t_reports) and status=0"
    failed_sql = "select * from t_reports where version in" \
                 " (select max(version) as version from t_reports) and status!=0"
    success_results = dbfucs.query(success_sql)
    failed_results = dbfucs.query(failed_sql)
    for result in (success_results, failed_results):
        for r in result:
            runtime = float(r.get("runtime"))
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


@bp.route("/conditionquerytestress", methods=["post"])
def conditionquerytestres():
    res = {}
    res["code"] = 200
    res["data"] = _get_test_results_by_conditions(**request.get_json())
    res["msg"] = "查询成功!"
    return jsonify(res)
