# -*- coding:utf-8 -*-
__author__ = 'snake'

import os
from app import bp
from flask import jsonify, request
from app.utils.log import Logger
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
        print(testcases)
        # 解析并导入用例
        moduleid = request.form.get("moduleid")

        # todo 这里导入的数据有问题，表现为没有moduleid，如果一个har有多个case，那么moduleid无法判断，尴尬！！！

    else:
        return jsonify({"code": -100, "msg": "上传失败"})

    return "123"
