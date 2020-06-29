# coding: utf-8
import os
import sys
from base.helpers import dingtalk_helper
from base.utils import config_utils


sys_args = sys.argv
build_user_id = sys_args[1]
jenkins_url = sys_args[2]
job_name = sys_args[3]
build_id = sys_args[4]
execute_result = sys_args[5]
result_dingtalk_token = sys_args[6]
if len(sys_args) > 7 and sys_args[7]:
    branch = sys_args[7]
else:
    branch = ""
config_file = os.getenv("PYTHONPATH", "/root/PycharmProjects/PythonDemo") + "/jenkins/config/config.ini"
at_phone = config_utils.getConfig(config_file, "build_users_phone", build_user_id, fallback="")
print("build_user_id = %s, at_phone = %s" % (build_user_id, at_phone))
if at_phone:
    at_phone_msg = " @" + at_phone
    at_mobile_list = [at_phone]
else:
    at_phone_msg = ""
    at_mobile_list = []

job_url = jenkins_url + "job/" + job_name + "/"
build_url = job_url + build_id
if branch:
    branch_msg = "(" + branch + ")"
else:
    branch_msg = ""
body = {
    "actionCard": {
        "title": job_name,
        "text": "[" + job_name + "]" + "("+job_url + ")" + branch_msg + " [#" + build_id + "]" + "("+build_url + ")" +
                " execute " + execute_result + at_phone_msg
    },
    "at": {
        "atMobiles": at_mobile_list,
        "isAtAll": False
    },
    "msgtype": "actionCard"
}

dingtalk_helper.send_body(body, result_dingtalk_token)
