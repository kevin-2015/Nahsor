# -*- conding:utf-8 -*-
'''
模块管理的相关接口
'''
__author__ = "Jin"
from flask import jsonify, request
from app import bp
from app.utils import dbfucs
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


@bp.route("/getproject",methods=["GET"])
def getproject():
    '''
    读取产品列表，这个接口是给新增项目等东西的时候，选择所属产品用的
    '''
    sql = "SELECT * FROM t_project"
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/addproject",methods=["POST"])
def addproject():
    '''
    新增项目
    {
        "moduleid":"所属产品id",
        "project":"项目名称",
        "explain":"描述",
        "leader":"责任人",
        "remark":"备注"
    }
    '''
    dictdata = request.get_json()
    moduleid = dictdata["moduleid"]
    project = dictdata["project"]
    explain = dictdata["explain"]
    leader = dictdata["leader"]
    remark = dictdata["remark"]
    sql = "insert into t_project values(null,'%s','%s','%s','%s','%s',null,null);" % (moduleid,project,explain,leader,remark)
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "新增成功！！！"
    return jsonify(response)


@bp.route("/queryproject",methods=["GET"])
def queryproject():
    '''
    查询项目列表
    '''
    sql = "SELECT\
        t_project.id,\
        t_project.project,\
        t_project.`explain`,\
        (SELECT COUNT(*) FROM t_modules WHERE projectid = t_project.id) AS modulenum,\
        (SELECT COUNT(*) FROM t_testcass WHERE projectid = t_project.id) AS cassnum,\
        t_project.leader,\
        t_project.remark,\
        t_project.createtime,\
        t_project.updatatime\
        FROM\
        t_project"
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/deleteproject",methods=["POST"])
def deleteproject():
    '''
    删除项目
    {"pid":1}
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    sql = "DELETE FROM `t_project` WHERE (`id`='%s')" % pid
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "删除成功！！！"
    return jsonify(response)


@bp.route("/readproject",methods=["POST"])
def readproject():
    '''
    读取项目信息
    {"pid":1}
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    sql = "SELECT\
        t_project.moduleid,\
        t_project.project,\
        t_project.`explain`,\
        t_project.leader,\
        t_project.remark,\
        t_project.moduleid\
        FROM\
        t_project\
        WHERE\
        t_project.id = %s" % pid
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/updataproject",methods=["POST"])
def updataproject():
    '''
    更新产品信息
    {
        "pid":2,
        "project":"产品名称",
        "explain":"描述",
        "leader":"责任人",
        "remark":"备注"
    }
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    moduleid = dictdata["moduleid"]
    project = dictdata["project"]
    explain = dictdata["explain"]
    leader = dictdata["leader"]
    remark = dictdata["remark"]
    sql = "UPDATE `t_project`\
        SET `moduleid` = '%s',\
        `project` = '%s',\
        `explain` = '%s',\
        `leader` = '%s',\
        `remark` = '%s'\
        WHERE (`id` = '%s')" % (moduleid,project, explain, leader, remark, pid)
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "更新成功！！！"
    return jsonify(response)


@bp.route("/runproject",methods=["POST"])
def runproject():
    '''
    按产品执行所有用例
    {"idlist":"1,2"}
    '''
    dictdata = request.get_json()
    idlist = dictdata["idlist"]
    sql = "SELECT * FROM t_testcass WHERE projectid in (%s)" % idlist
    res = dbfucs.query(sql)
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
