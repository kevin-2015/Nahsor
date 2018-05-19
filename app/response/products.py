# -*- conding:utf-8 -*-
'''
产品管理的相关接口
'''
__author__ = "Jin"
from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


@bp.route("/addproduct",methods=["POST"])
def addproduct():
    '''
    新增产品
    {
        "product":"Nahsor自动化测试平台",
        "explain":"一个接口自动化测试平台，功能强大，很厉害就是了。",
        "leader":"浪晋",
        "remark":"这是例子"
    }
    '''
    dictdata = request.get_json()
    product = dictdata["product"]
    explain = dictdata["explain"]
    leader = dictdata["leader"]
    remark = dictdata["remark"]
    now = common.get_current_time()
    sql = "insert into t_product " \
          "values(null,'%s','%s','%s','%s','%s',null);" \
          % (product,explain,leader,remark, now)
    print(sql)
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "新增成功！！！"
    return jsonify(response)


@bp.route("/queryproduct",methods=["GET"])
def queryproduct():
    '''
    查询产品列表
    '''
    sql = "SELECT\
                a.id as productid,\
                a.product,\
                a.`explain`,\
                ( SELECT COUNT( * ) FROM t_project WHERE t_project.productid = a.id ) AS jectnum,\
                count(c.id) as modulenum,\
                a.leader,\
                a.remark,\
                a.createtime,\
                a.updatatime\
        FROM\
              t_product AS a\
        LEFT JOIN t_project as b ON a.id = b.productid\
        LEFT JOIN t_modules as c ON c.projectid = b.id\
        GROUP BY\
              a.id	"
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/deleteproduct",methods=["POST"])
def deleteproduct():
    '''
    删除产品，产品下面的所有关联的内容都会被删除
    {"pid":1}
    '''
    dictdata = request.get_json()
    # 查询产品id
    pid = dictdata["pid"]

    # 查询项目id询 模块id 用例id
    sql = "SELECT\
                a.id AS projectid,\
                b.id AS moduleid,\
                c.id AS testcaseid \
            FROM\
                t_project AS a\
                LEFT JOIN t_modules AS b ON a.id = b.projectid\
                LEFT JOIN t_testcass AS c ON c.moduleid = b.id\
            WHERE\
	            a.productid = %s" % pid

    # 级联删除 case -> module -> project -> product
    for ids in dbfucs.query(sql):
        delete_modelus_sql = "delete from t_modules where id = %d" % ids.get("moduleid")
        delete_testcase_sql = "delete from t_testcass where id = %d" % ids.get("testcaseid")
        delete_project_sql = "delete from t_project where id = %d" % ids.get("projectid")
        dbfucs.excute(delete_testcase_sql)
        dbfucs.excute(delete_modelus_sql)
        dbfucs.excute(delete_project_sql)

    sql = "DELETE FROM `t_product` WHERE (`id`='%s')" % pid
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "删除成功！！！"
    return jsonify(response)


@bp.route("/readproduct",methods=["POST"])
def readproduct():
    '''
    读取产品信息
    {"pid":1}
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    sql = "SELECT\
        t_product.product,\
        t_product.`explain`,\
        t_product.leader,\
        t_product.remark\
        FROM\
        t_product\
        WHERE\
        t_product.id = %s" % pid
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)


@bp.route("/updataproduct",methods=["POST"])
def updataproduct():
    '''
    更新产品信息
    {
        "pid":2,
        "product":"产品名称",
        "explain":"描述",
        "leader":"责任人",
        "remark":"备注"
    }
    '''
    dictdata = request.get_json()
    pid = dictdata["pid"]
    product = dictdata["product"]
    explain = dictdata["explain"]
    leader = dictdata["leader"]
    remark = dictdata["remark"]
    sql = "UPDATE `t_product`\
        SET `product` = '%s',\
        `explain` = '%s',\
        `leader` = '%s',\
        `remark` = '%s'\
        WHERE (`id` = '%s')" % (product, explain, leader, remark, pid)
    res = dbfucs.excute(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "更新成功！！！"
    return jsonify(response)


@bp.route("/runproduct",methods=["POST"])
def runproduct():
    '''
    按产品执行所有用例
    {"idlist":"1,2"}
    '''
    dictdata = request.get_json()
    idlist = dictdata["idlist"]
    sql = "SELECT\
        t_testcass.*\
    FROM\
        t_product\
    LEFT JOIN t_project ON t_product.id = t_project.productid\
    LEFT JOIN t_modules ON t_project.id = t_modules.projectid\
    LEFT JOIN t_testcass ON t_modules.id = t_testcass.moduleid\
    WHERE t_product.id in (%s);" % idlist
    print(sql)
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
