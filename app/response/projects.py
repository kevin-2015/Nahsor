# -*- conding:utf-8 -*-
'''
项目管理的相关接口
'''
__author__ = "Jin"
from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


@bp.route("/getproduct",methods=["GET"])
def getproduct():
    '''
    读取产品列表，这个接口是给新增项目等东西的时候，选择所属产品用的
    '''
    sql = "SELECT id,product FROM t_product"
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
        "productid":"5",
        "project":"Nahsor自动化测试平台WEB端",
        "explain":"功能强大，厉害的不行",
        "leader":"浪晋",
        "remark":"没有备注"
    }
    '''
    dictdata = request.get_json()
    productid = dictdata["productid"]
    project = dictdata["project"]
    explain = dictdata["explain"]
    leader = dictdata["leader"]
    remark = dictdata["remark"]
    now = common.get_current_time()
    sql = "insert into t_project " \
          "values(null,'%s','%s','%s','%s','%s','%s',null);" \
          % (productid,project,explain,leader,remark,now)
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "新增成功！！！"
    return jsonify(response)


@bp.route("/queryproject",methods=["GET"])
def queryproject():
    '''
    查询项目列表，还需要改进搜索的功能
    '''
    sql = "SELECT\
        t_project.id as projectid,\
        t_project.productid,\
        t_project.project,\
        t_project.`explain`,\
        (SELECT COUNT(*) FROM t_modules WHERE t_modules.projectid = t_project.id) AS modulenum,\
        count(t_testcass.id) AS cassnum,\
        t_project.leader,\
        t_project.remark,\
        t_project.createtime,\
        t_project.updatatime\
    FROM\
        t_project\
    LEFT JOIN t_modules ON t_project.id = t_modules.projectid\
    LEFT JOIN t_testcass ON t_modules.id = t_testcass.moduleid\
    group by t_project.id;"
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)



@bp.route("/deleteproject",methods=["POST"])
def deleteproject():
    '''
    删除项目，项目下面的所有关联的内容都会被删除
    {"pid":1}
    '''
    dictdata = request.get_json()
    # 查询产品id
    pid = dictdata["pid"]

    # 查询项目id询 模块id 用例id
    sql = "SELECT\
                a.id AS moduleid,\
                b.id AS testcaseid \
            FROM\
                t_modules AS a\
                LEFT JOIN t_testcass AS b ON b.moduleid = a.id \
            WHERE\
                a.projectid = %s" % pid

    # 级联删除 case -> module -> project
    for ids in dbfucs.query(sql):
        delete_modelus_sql = "delete from t_modules where id = %d" % ids.get("moduleid")
        delete_testcase_sql = "delete from t_testcass where id = %d" % ids.get("testcaseid")
        dbfucs.excute(delete_testcase_sql)
        dbfucs.excute(delete_modelus_sql)

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
        t_project.productid,\
        t_project.project,\
        t_project.`explain`,\
        t_project.leader,\
        t_project.remark,\
        t_project.productid\
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
        "pid":5,
        "productid":5,
        "project":"Nahsor自动化测试平台WEB端",
        "explain":"功能强大，厉害的不行",
        "leader":"浪晋",
        "remark":"备注"
    }
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    productid = dictdata["productid"]
    project = dictdata["project"]
    explain = dictdata["explain"]
    leader = dictdata["leader"]
    remark = dictdata["remark"]
    sql = "UPDATE `t_project`\
        SET `productid` = '%s',\
        `project` = '%s',\
        `explain` = '%s',\
        `leader` = '%s',\
        `remark` = '%s'\
        WHERE (`id` = '%s')" % (productid,project, explain, leader, remark, pid)
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "更新成功！！！"
    return jsonify(response)


@bp.route("/runproject",methods=["POST"])
def runproject():
    '''
    按项目执行所有用例
    {"idlist":"1,2"}
    '''
    dictdata = request.get_json()
    idlist = dictdata["idlist"]
    ids = ''
    for i in idlist:
        ids += str(i) + ","
    sql = "SELECT\
        t_testcass.*\
    FROM\
        t_project\
    LEFT JOIN t_modules ON t_project.id = t_modules.projectid\
    LEFT JOIN t_testcass ON t_modules.id = t_testcass.moduleid\
    WHERE t_project.id in (%s)" % ids[:-1]
    res = dbfucs.query(sql)

    if len(res) == 0:
        response = {}
        response["code"] = 200
        response["msg"] = "没有可用用例执行"
        return jsonify(response)
    idlist = []
    for i in res:
        idlist.append(i['id'])
    ids = ''
    for i in idlist:
        ids += str(i) + ","
    sql = "select id,testname,testtype,request,validate,extract from t_testcass where id in(%s);" % ids[:-1]
    res = dbfucs.query(sql)

    jsoncasss = []
    for test in res:
        jsoncasss.append(test)
    for i in collect.collect_db_cass(jsoncasss):
        Logger.info("*" * 90)
    Logger.info("共计[%d]条测试用例执行完成！" % len(jsoncasss))
    Logger.info("*" * 90)
    response = {}
    response["code"] = 200
    response["msg"] = "成功！！！"
    return jsonify(response)
