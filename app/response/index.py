# -*- conding:utf-8 -*-
__author__ = "snake"

from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


@bp.route("/index", methods=["get"])
def index():
    """
    后台首页统计图接口
    1. 上次用例执行成功/失败图
    2. 上次用例执行时间分段统计图
    3. 每个项目的模块统计
    4. 每个模块的用例统计


    :return:
    """

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
          " (select max(version) as version from t_reports) and status=0"
    failed_sql = "select * from t_reports where version in" \
          " (select max(version) as version from t_reports) and status!=0"
    success_results = dbfucs.query(success_sql)
    failed_results = dbfucs.query(failed_sql)

    last_testreports = {}
    last_testreports["success"] = {"data":success_results, "count":len(success_results)}
    last_testreports["failed"] = {"data":failed_results, "count":len(failed_results)}

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


    """
        3. 每个项目的模块统计
        {"modulescount":
           [{"project1":{}, "modules":[{},{}], "count":1}, 
           {"project2":{}, "modules":[{},{}]}, "count":1]
        } 
    """
    ## 为什么没有第二个module信息呢
    modulescount = []
    sql = "select projectid from t_modules GROUP BY projectid"
    for results in dbfucs.query(sql):
        singeitem = {}

        # 统计count和modules
        id = results.get("projectid")
        sql = "select * from t_modules where id = %d" % id
        res = dbfucs.query(sql)
        if res:
            singeitem["count"] = len(res)# count
            singeitem["modules"] = res   # modules
            projectid = res[0].get("projectid")

            # 统计project
            sql = "select * from t_project where id = %d" % projectid
            res = dbfucs.query(sql)
            if res:
                singeitem["project"] = res[0]

            modulescount.append(singeitem)

    response = {}
    response["testreports"] = last_testreports
    response["runtimecount"] = {"faster": faster, "fast": fast, "slow": slow, "slowly": slowly}
    response["modulescount"] = modulescount
    return jsonify({"datas": response})
