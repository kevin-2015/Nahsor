# -*- coding:utf-8 -*-
__author__ = 'snake'

import os, json
from app import bp
from flask import jsonify, request
from app.utils.log import Logger
from app.utils.common import get_current_time
from app.utils.dbfucs import excute
from app.utils.jsonfuc import validate_req_by_file
Logger = Logger()


def _upload_files(file):
    """
    上传图片公共方法
    :param file: 上传的file文件
    :return: True:成功;False失败
    """
    try:
        upload_path = os.path.join("./app/uploads/", file.filename)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        file.save(upload_path)
        return True
    except:
        return False


@bp.route("/uploadtestcase", methods=['POST'])
def uploadtestcase():
    file = request.files['file']
    filetype = file.filename.split(".")[1]
    if filetype != "har":
        filetype = "postman"

    # 上传并解析
    if _upload_files(file):
        testcases = validate_req_by_file(
            file_path=os.path.join("./app/uploads/", file.filename), type=filetype)

        # 需要对应的postman和har的请求中包含以下字段
        failed, success = 0, 0
        for case in testcases:
            moduleid = case.get("moduleid")
            testname = case.get("testname")
            testtype = case.get("testtype")
            explain = case.get("explain")
            requests = case.get("request")
            validate = case.get("validate")
            extract = case.get("extract")
            leader = case.get("leader")
            remark = case.get("remark")

            # 插入sql数据
            sql = "insert into t_testcass \
            (`moduleid`, `testname`, `testtype`, `explain`, \
            `request`, `validate`, `extract`, `leader`, `remark`, `createtime`) \
            values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');\
            " % (moduleid, testname, testtype, explain, requests, validate, extract, leader, remark, get_current_time())
            if excute(sql):
                success += 1
            else:
                failed += 1

        res = {
            "code": 200,
            "msg": "执行成功,成功导入%s个,失败%s个" % (success, failed)
        }
        return jsonify(res)
    else:
        return jsonify({"code": -100, "msg": "上传失败"})
