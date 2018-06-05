# -*- conding:utf-8 -*-
__author__ = "snake"

from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


def _get_test_results(**kwargs):
    """
    抽象查询结果的公共方法
    :params kwargs: 参数可以传任意值
        {} / {"version": 14} / {"version": 14, "productid": 1}
        {"version": 14, "productid": 1, "projectid": 1} / {"version": 14, "productid": 1, "projectid": 1, "moduleid": 6}
    :return:
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

    all_sql = "SELECT a.* FROM t_reports AS a %s %s  %s ,t_testcass as e WHERE %s %s %s %s" \
                  " AND a.cassid = e.id" % (product_sql[0], project_sql[0], module_sql[0], version_sql, product_sql[1], project_sql[1], module_sql[1])

    return dbfucs.query(success_sql), dbfucs.query(failed_sql), dbfucs.query(all_sql)


@bp.route("/conditionqueryreports", methods=['post'])
def conditionsqueryreports():
    """
    获取根据版本获取用例执行结果
    {"version":""}：默认最大
    {"version":5}：版本为5的报告
    :return:
    """
    success_results, failed_results, all_results = _get_test_results(**request.get_json())
    response = {"code": 200, "data": all_results, "msg": "查询成功！！！"}
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


@bp.route("/conditionquerytestress", methods=["post"])
def conditionquerytestres():
    """
    条件查询测试结果
    :param   参数可以传任意值
    {} / {"version": 14} / {"version": 14, "productid": 1}
    {"version": 14, "productid": 1, "projectid": 1} / {"version": 14, "productid": 1, "projectid": 1, "moduleid": 6}
    :return:
    """
    """ 返回值:
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
    res, last_testreports = {}, {}
    success_results, failed_results, all_results = _get_test_results(**request.get_json())
    last_testreports["success"] = {"data": success_results, "count": len(success_results)}
    last_testreports["failed"] = {"data": failed_results, "count": len(failed_results)}

    response = {"code": 200, "data": last_testreports, "msg": "查询成功！！！"}
    return jsonify(response)



@bp.route("/conditionqueryruntimes", methods=["post"])
def conditionqueryruntimes():
    """
    条件查询用例执行时间分段统计图
    :param ： 可以传以下任意参数
    {} / {"version": 14} / {"version": 14, "productid": 1}
    {"version": 14, "productid": 1, "projectid": 1} / {"version": 14, "productid": 1, "projectid": 1, "moduleid": 6}
    : return :
    """
    """
        时间分段统计：
        极快: t<1s
        快速: 1s< t <3s
        慢: 3s < t < 5s
        超级慢: t>5s

     {
        "code": 200,
        "data": {
            "fast": {
                "count": 0,
                "times": []
            },
            "faster": {
                "count": 0,
                "times": []
            },
            "slow": {
                "count": 0,
                "times": []
            },
            "slowly": {
                "count": 2,
                "times": [
                    100,
                    100
                ]
            }
        },
        "msg": "查询成功!"
}
    """

    # 各个参数
    res, last_testreports, faster, fast, slow, slowly = {}, {}, {}, {}, {}, {}
    faster["count"], fast["count"], slow["count"], slowly["count"] = 0, 0, 0, 0
    faster["times"], fast["times"], slow["times"], slowly["times"], = [], [], [], []
    success_results, failed_results, all_results = _get_test_results(**request.get_json())
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

    # 返回值
    res["code"] = 200
    res["data"] = {"faster": faster, "fast": fast, "slow": slow, "slowly": slowly}
    res["msg"] = "查询成功!"
    return jsonify(res)