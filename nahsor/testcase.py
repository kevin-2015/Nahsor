# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：解析json为用例的各种方法
'''
import json
from logger import Logger
import exception
logger = Logger()


def import_json_file(filename):
    '''
    filename = "test_*.json"
    说明：判断导入的json文件名/格式是否合法
    '''
    filetype = filename.split(".")
    if filetype[-1] == "json" and filename.startswith("test"):
        return filename
    else:
        logger.error("{}导入的JSON文件格式不正确，请检查JSON格式！".format(filename))
        exit()


def chick_type_json(filename):
    '''
    检查json文件的内容
    {
        "testcase": {
            "name": "teatname",
            "request": {
                "url": "http://127.0.0.1/test",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "json": {
                    "username": "admin",
                    "password":"123456"
                }
            },
            "extract": [
                {"token": "$token"}
                ],
            "validate": [
                {"eq": ["status_code", 200]}
                ]
            }
    }
    '''
    with open(filename, 'r') as f:
        json_context = json.load(f)
        # print(json_context)
    if not isinstance(json_context, dict):
        raise exception.NotFoundCaseError("用例格式错误，json数据不是list")
    if len(json_context) == 0:
        raise exception.NotFoundCaseError("在json文件中没有找到testcase")
    return json_context


def get_request_args(rspec, test_block_config):
    """Format the test spec given values inthe global config

    Todo:
        Add similar functionality to validate/save $ext functions so input
        can be generated from a function

    Args:
        rspec (dict): Test spec
        test_block_config (dict): Test block config

    Returns:
        dict: Formatted test spec

    Raises:
        BadSchemaError: Tried to pass a body in a GET request
    """

    request_args = {}

    # Ones that are required and are enforced to be present by the schema
    required_in_file = [
        "method",
        "url",
    ]

    optional_in_file = [
        "json",
        "data",
        "params",
        "headers",
        "files"
        # Ideally this would just be passed through but requests seems to error
        # if we pass a list instead of a tuple, so we have to manually convert
        # it further down
        # "auth",
    ]

    optional_with_default = {
        "verify": True,
    }

    if "method" not in rspec:
        logger.debug("Using default GET method")
        rspec["method"] = "GET"

    headers = rspec.get("headers")
    if headers:
        if "content-type" not in [h.lower() for h in headers.keys()]:
            rspec["headers"]["content-type"] = "application/json"

    fspec = format_keys(rspec, test_block_config["variables"])

    def add_request_args(keys, optional):
        for key in keys:
            try:
                request_args[key] = fspec[key]
            except KeyError:
                if optional or (key in request_args):
                    continue

                # This should never happen
                raise

    add_request_args(required_in_file, False)
    add_request_args(optional_in_file, True)

    if "auth" in fspec:
        request_args["auth"] = tuple(fspec["auth"])

    for key in optional_in_file:
        try:
            func = get_wrapped_create_function(request_args[key].pop("$ext"))
        except (KeyError, TypeError):
            pass
        else:
            request_args[key] = func()

    # If there's any nested json in parameters, urlencode it
    # if you pass nested json to 'params' then requests silently fails and just
    # passes the 'top level' key, ignoring all the nested json. I don't think
    # there's a standard way to do this, but urlencoding it seems sensible
    # eg https://openid.net/specs/openid-connect-core-1_0.html#ClaimsParameter
    # > ...represented in an OAuth 2.0 request as UTF-8 encoded JSON (which ends
    # > up being form-urlencoded when passed as an OAuth parameter)
    for key, value in request_args.get("params", {}).items():
        if isinstance(value, dict):
            request_args["params"][key] = quote_plus(json.dumps(value))

    for key, val in optional_with_default.items():
        request_args[key] = fspec.get(key, val)

    # TODO
    # requests takes all of these - we need to parse the input to get them
    # "cookies",

    # These verbs _can_ send a body but the body _should_ be ignored according
    # to the specs - some info here:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    if request_args["method"] in ["GET", "HEAD", "OPTIONS"]:
        if any(i in request_args for i in ["json", "data"]):
            warnings.warn("You are trying to send a body with a HTTP verb that has no semantic use for it", RuntimeWarning)

    return request_args
