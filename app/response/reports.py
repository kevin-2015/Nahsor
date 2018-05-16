# -*- conding:utf-8 -*-
__author__ = "snake"

from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


@bp.route("/getreports", methods=['get'])
def getreports():
    sql = "SELECT * FROM t_reports"
    res = dbfucs.query(sql)
    response = {}
    response["code"] = 200
    response["data"] = res
    response["msg"] = "查询成功！！！"
    return jsonify(response)





