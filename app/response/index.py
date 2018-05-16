# -*- conding:utf-8 -*-
__author__ = "snake"

from flask import jsonify, request
from app import bp
from app.utils import dbfucs, common
from app.core import collect
from app.utils.log import Logger
Logger = Logger()


@bp.route("/index")
def index():
    """
    后台首页统计图接口
    1. 上次用例执行成功/失败图
    2. 上次用例执行时间分段统计图
    3. 每个项目的用例统计
    4. 每个模块的用例统计


    :return:
    """
    return