import json


def getCookies(driver):
    cookie_list = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookie_str = '; '.join(item for item in cookie_list)
    return cookie_str

