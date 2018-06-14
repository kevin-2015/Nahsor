# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：封装了requests的方法
'''
import requests
from logger import Logger
# from exception import NotFoundMethodError
requests.packages.urllib3.disable_warnings()
logger = Logger()

def httptest(request):
    '''
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
    '''
    
    url = request.pop("url")
    method = request.pop("method")
    kwargs = request
    # print(kwargs)
    try:
        response = requests.request(method,url,**kwargs)
        return response
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as timeout:
        logger.error("接口连接超时")



class RestRequest(BaseRequest):

    def __init__(self, session, rspec, test_block_config):
        """Prepare request

        Args:
            rspec (dict): test spec
            test_block_config (dict): Any configuration for this the block of
                tests

        Raises:
            UnexpectedKeysError: If some unexpected keys were used in the test
                spec. Only valid keyword args to requests can be passed
        """

        if 'meta' in rspec:
            meta = rspec.pop('meta')
            if meta and 'clear_session_cookies' in meta:
                session.cookies.clear_session_cookies()

        expected = {
            "method",
            "url",
            "headers",
            "data",
            "params",
            "auth",
            "json",
            "verify",
            "files",
            # "cookies",
            # "hooks",
        }

        check_expected_keys(expected, rspec)

        request_args = get_request_args(rspec, test_block_config)

        logger.debug("Request args: %s", request_args)

        request_args.update(allow_redirects=False)

        self._request_args = request_args

        # There is no way using requests to make a prepared request that will
        # not follow redirects, so instead we have to do this. This also means
        # that we can't have the 'pre-request' hook any more because we don't
        # create a prepared request.

        def prepared_request():
            # If there are open files, create a context manager around each so
            # they will be closed at the end of the request.
            with ExitStack() as stack:
                for key, filepath in self._request_args.get("files", {}).items():
                    self._request_args["files"][key] = stack.enter_context(
                            open(filepath, "rb"))
                return session.request(**self._request_args)

        self._prepared = prepared_request

    def run(self):
        """ Runs the prepared request and times it

        Todo:
            time it

        Returns:
            requests.Response: response object
        """

        try:
            return self._prepared()
        except requests.exceptions.RequestException as e:
            logger.exception("Error running prepared request")
            raise_from(exceptions.RestRequestException, e)

    @property
    def request_vars(self):
        return Box(self._request_args)
