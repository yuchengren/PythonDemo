import base64
import json

import requests

from base.api import baidu_apis


def getAccessToken(api_key, secret_key):
    url = baidu_apis.get_access_token % (api_key, secret_key)
    response = requests.get(url)
    if response:
        print("url=%s\nresult=%s" % (url, response.json()))
        return response.json()["access_token"]
    return None


def postImageTextRecognize(image_file, access_token):
    if not access_token:
        raise Exception("access_token is empty")
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    url = baidu_apis.post_text_recognise + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=params, headers=headers)
    if response:
        print("url=%s\nresult=%s" % (url, response.json()))
        return response.json()["words_result"][0]["words"]
    return None


def postTextRecognize(path: str, access_token):
    if not access_token:
        raise Exception("access_token is empty")
    if path.startswith("http") or path.startswith("https"):
        params = {"url": path}
    else:
        f = open(path, 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img}
    params["language_type"] = "ENG"
    url = baidu_apis.post_text_recognise + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=params, headers=headers)
    if response:
        print("url=%s\nparams=%s\nresult=%s" % (url, params, response.json()))
        return response.json()["words_result"][0]["words"]
    return None
