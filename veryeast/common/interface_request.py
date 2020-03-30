import requests

from veryeast.config import veryeast_config


def request(driver, path, param_dict):
    url = veryeast_config.HOST + path
    headers = {

    }
    response = requests.post(url, data=param_dict, headers=headers)
