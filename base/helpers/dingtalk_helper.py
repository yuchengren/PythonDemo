# coding: utf-8
import os
import json


def send_body(body, dingtalk_token):
    dataJson = json.dumps(body)
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + dingtalk_token
    send_cmd = "curl -H \'Content-Type: application/json\' -d \'" + dataJson + "\' " + url
    resp = os.popen(send_cmd).read()
    print(resp)
    return resp


def is_resp_success(resp):
    resp_json = json.loads(resp)
    return resp_json["errcode"] == 0

