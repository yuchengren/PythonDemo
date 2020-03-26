import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from android.market.config import market_accounts
from base.config import email_urls
from base.selenium import ElementUtils
from base.utils import TimeUtils

captcha_check_interval = 5 * 60


def login(driver: WebDriver, username, password):
    main_window = driver.current_window_handle
    driver.execute_script('window.open("%s");' % email_urls.aliyun_enterprise_email_login_url)
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break
    login_iframe_parent = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "login_panel_iframe")))
    driver.switch_to.frame(login_iframe_parent)
    login_iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ding-login-iframe")))
    driver.switch_to.frame(login_iframe)
    login_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "login_submit_btn")))
    driver.find_element_by_id("username").send_keys(username)
    captcha_element = ElementUtils.findElement(driver, By.ID, "login_checkcode")
    if captcha_element is not None:
        while login_btn is not None:
            login_btn = inputPasswordAndCapture(driver, password)
    else:
        driver.find_element_by_id("password").send_keys(password)
        login_btn.click()
        time.sleep(2)
    driver.switch_to.default_content()
    return main_window


def inputPasswordAndCapture(driver: WebDriver, password):
    captcha_element = ElementUtils.findElement(driver, By.ID, "login_checkcode")
    login_btn = ElementUtils.findElement(driver, By.ID, "login_submit_btn")
    inputPasswordElement = driver.find_element_by_id("password")
    if len(inputPasswordElement.get_attribute('value').strip()) == 0:
        inputPasswordElement.send_keys(password)
        time.sleep(0.2)
        captcha_element = ElementUtils.findElement(driver, By.ID, "login_checkcode")
        if captcha_element is not None:
            driver.execute_script("arguments[0].focus();", captcha_element)
    time.sleep(5)
    if len(captcha_element.get_attribute('value').strip()) == 4:
        # 加载loading id="spin" class="spinner"
        login_btn.click()
        time.sleep(2)
        login_btn = ElementUtils.findElement(driver, By.ID, "login_submit_btn")
    return login_btn


def getCaptcha(driver: WebDriver, isFirstGet, title_filter, content_filter):
    receive_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "treenode_item_text_sel")))  # 收件箱
    content_div = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "maillist_content_wrap")))
    if not isFirstGet:
        time.sleep(5)
        receive_box.click()
    time.sleep(0.1)
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "maillist_virtual_inline_loading_text")))

    email_list = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "maillist_virtual_block")))
    email_items = email_list.find_elements_by_class_name("maillist_item_hassummary")
    text = ""
    for item in email_items:
        item_time_element = item.find_element_by_class_name("maillist_item_time").find_element_by_class_name("ellipsis")
        item_time_text = item_time_element.get_attribute("_title")  # 2020年2月8日(星期六) 16:13
        item_time_text_black_list = item_time_text.split(" ")
        item_time_str = item_time_text_black_list[1]
        item_date_str = item_time_text_black_list[0].split("(")[0]
        item_date_time = TimeUtils.parseToDatetime(item_date_str + " " + item_time_str, "%Y年%m月%d日 %H:%M")
        interval_now_seconds = abs((datetime.now() - item_date_time).seconds)

        if title_filter in item.find_element_by_class_name("maillist_item_rcp_inner").text and \
                content_filter in item.find_element_by_class_name("maillist_item_summary_inner").text and \
                interval_now_seconds < captcha_check_interval:
            item.click()
            email_content_iframe = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "read_iframe")))
            driver.switch_to.frame(email_content_iframe)
            captcha_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "b")))
            text = captcha_element.text.strip()
            driver.switch_to.default_content()
            if len(text) != 0:
                print("%s %s %s" % (title_filter, content_filter, text))
                return text
    return text


def loginAndGetCaptcha(driver: WebDriver, username, password, title_filter, content_filter):
    main_window = login(driver, username, password)
    captcha = ""
    isFirstGet = True
    while len(captcha) == 0:
        captcha = getCaptcha(driver, isFirstGet, title_filter, content_filter)
        isFirstGet = False
    driver.switch_to.window(main_window)
    return captcha


if __name__ == '__main__':
    driver = webdriver.Chrome()
    loginAndGetCaptcha(driver, market_accounts.oppo_market_username, market_accounts.oppo_market_password, "OPPO", "验证码")