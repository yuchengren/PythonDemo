import json
import time

import requests

import base.config.account
from base.selenium import CookieUtils
from veryeast.config import veryeast_config


def post(path, cookie_dict, param_dict, jsession_id=""):
    url = veryeast_config.HOST + path
    cookie_str = CookieUtils.getCookieStrFromDict(cookie_dict)
    cookie_str = "JSESSIONID=%s; %s" % (jsession_id, cookie_str)
    cookie_dict["JSESSIONID"] = jsession_id
    _headers = {"admin-token": cookie_dict["admin-token"],
                "content_Type": "multipart/form-data",
                "x-requested-with": "XMLHttpRequest",
                "Cookie": cookie_str}
    param_dict["token"] = base.config.account.veryeast_username
    param_dict["loginName"] = base.config.account.veryeast_username
    before_request_time = time.time()
    response = requests.post(url, data=param_dict, headers=_headers)
    print("path=%s,request_time = %f,response=%s" % (path, (time.time() - before_request_time), response.text))
    return json.loads(response.text)
