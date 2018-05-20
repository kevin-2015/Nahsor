# -*- conding:utf-8 -*-
'''
模块管理的相关接口
'''
__author__ = "Jin"
from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


@bp.route("/getproject",methods=["GET"])
def getproject():
    '''
    读取项目列表，这个接口是给新增模块等东西的时候，选择所属项目用的
    '''
    sql = "SELECT t_product.id as productid, t_product.product FROM t_product"
    res = dbfucs.query(sql)
    projelist = []
    for prod in res:
        sql = "SELECT t_project.id as projectid, t_project.project FROM t_project where productid = %s" % prod["productid"] 
        res = dbfucs.query(sql)
        prod["jectinfo"] = res
        projelist.append(prod)
    response = {}
    response["code"] = 200
    response["data"] = projelist
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/addmodule",methods=["POST"])
def addmodule():
    '''
    新增模块
    {
        "projectid":"所属项目id",
        "module":"模块名称",
        "explain":"描述",
        "leader":"责任人",
        "remark":"备注"
    }
    '''
    dictdata = request.get_json()
    projectid = dictdata["projectid"]
    module = dictdata["module"]
    explain = dictdata["explain"]
    leader = dictdata["leader"]
    remark = dictdata["remark"]
    sql = "insert into " \
          "t_modules " \
          "values(null,'%s','%s','%s','%s','%s','%s',null);" \
          % (projectid, module, explain, leader, remark, common.get_current_time())

    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "新增成功！！！"
    return jsonify(response)


@bp.route("/querymodule",methods=["GET"])
def querymodule():
    '''
    查询模块列表
    '''
    sql = "SELECT\
        t_modules.id as moduleid,\
        t_modules.modules,\
        t_modules.`explain`,\
        (SELECT COUNT(*) FROM t_testcass WHERE t_testcass.moduleid = t_modules.id) AS cassnum,\
        t_modules.leader,\
        t_modules.remark,\
        t_modules.createtime,\
        t_modules.updatatime\
    FROM\
        t_modules\
    LEFT JOIN t_testcass ON t_modules.id = t_testcass.moduleid\
    group by t_modules.id;"
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/deletemodule",methods=["POST"])
def deletemodule():
    '''
    删除模块
    {"pid":1}
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    delete_testcase_sql = "delete from t_testcass where moduleid=%s" % pid
    delete_modules_sql = "DELETE FROM `t_modules` WHERE (`id`='%s')" % pid

    response = {}
    response["code"] = 200
    response["data"] = dbfucs.excute(delete_testcase_sql)\
                            and dbfucs.excute(delete_modules_sql)
    response["msg"] = "删除成功！！！"
    return jsonify(response)


@bp.route("/readmodule",methods=["POST"])
def readmodule():
    '''
    读取模块信息
    {"pid":1}
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    sql = "SELECT\
        t_modules.id,\
        t_modules.modules,\
        t_modules.`explain`,\
        t_modules.leader,\
        t_modules.remark\
        FROM\
        t_modules\
        WHERE\
        t_modules.id = %s" % pid
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/updatamodule",methods=["POST"])
def updatamodule():
    '''
    更新模块信息
    {
    	"pid":4,
        "projectid":2,
        "module":"模块名称",
        "explain":"描述",
        "leader":"责任人",
        "remark":"备注"
    }
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    projectid = dictdata["projectid"]
    module = dictdata["module"]
    explain = dictdata["explain"]
    leader = dictdata["leader"]
    remark = dictdata["remark"]
    sql = "UPDATE `t_modules`\
        SET `projectid` = '%s',\
        `modules` = '%s',\
        `explain` = '%s',\
        `leader` = '%s',\
        `remark` = '%s', \
        `updatatime` = '%s'\
        WHERE (`id` = '%s')" % (projectid, module, explain, leader, remark, common.get_current_time(), pid)
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "更新成功！！！"
    return jsonify(response)


@bp.route("/runmodule",methods=["POST"])
def runmodule():
    '''
    按模块执行所有用例
    {"idlist":"1,2"}
    '''
    dictdata = request.get_json()
    idlist = dictdata["idlist"]
    ids = ''
    for i in idlist:
        ids += str(i) + ","
    sql = "SELECT * FROM t_testcass WHERE moduleid in (%s)" % ids[:-1]
    res = dbfucs.query(sql)
    if len(res) == 0:
        response = {}
        response["code"] = 200
        response["msg"] = "没有可用用例执行"
        return jsonify(response)
    jsoncasss = []
    for test in res:
        jsoncasss.append(test)
    # print(jsoncasss)
    for i in collect.collect_db_cass(jsoncasss):
        Logger.info("*" * 90)
    Logger.info("共计[%d]条测试用例执行完成！" % len(jsoncasss))
    Logger.info("*" * 90)
    response = {}
    response["code"] = 200
    response["msg"] = "成功！！！"
    return jsonify(response)
