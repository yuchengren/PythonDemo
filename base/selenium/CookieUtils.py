import json


def getCookiesStr(driver):
    cookie_list = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookie_str = '; '.join(item for item in cookie_list)
    return cookie_str


def getCookiesDict(driver):
    cookie_dict = {}
    for item in driver.get_cookies():
        cookie_dict[item["name"]] = item["value"]
    return cookie_dict
