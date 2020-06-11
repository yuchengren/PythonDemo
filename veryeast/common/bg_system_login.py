import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from base.api import tujian_api_helper
from base.config import account
from base.selenium import CookieUtils
from base.utils import TimeUtils
from veryeast.config import veryeast_config
from PIL import Image, ImageEnhance
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver: WebDriver, username, pwd, tujian_username=None, tujian_pwd=None):
    is_auto_recognise = tujian_username and tujian_pwd
    AUTO_RECOGNISE_MAX_COUNT = 5
    imgFilePath = veryeast_config.SCREEN_IMG_DIR + "/captcha.png"

    # 打开后台网址
    driver.get(veryeast_config.BG_SYSTEM_URL)

    width = driver.execute_script("return document.body.clientWidth")
    height = driver.execute_script("return document.body.clientHeight")
    print("driver width=%d height=%d" % (width, height))
    driver.set_window_size(width, height)
    # 输入用户名
    inputUserNameElement = driver.find_element_by_id("username")
    inputUserNameElement.send_keys(username)

    auto_recognise_count = 0
    loginElement = driver.find_element_by_id("butn")
    while loginElement is not None:
        if auto_recognise_count >= AUTO_RECOGNISE_MAX_COUNT:
            raise Exception("auto recognise captcha fail over %d " % AUTO_RECOGNISE_MAX_COUNT)
        inputPasswordElement = driver.find_element_by_id("password")
        verifyCodeElement = driver.find_element_by_id("Txtidcode")
        if len(inputPasswordElement.get_attribute('value').strip()) == 0:
            inputPasswordElement.send_keys(pwd)
            driver.execute_script("arguments[0].focus();", verifyCodeElement)
        if is_auto_recognise:
            verifyCode = recognize_captcha(driver, imgFilePath, tujian_username, tujian_pwd)
            auto_recognise_count += 1
            verifyCodeElement.send_keys(verifyCode)
        else:
            time.sleep(5)
        if len(verifyCodeElement.get_attribute('value').strip()) == 4:
            loginElement.click()
            time.sleep(1)
            # 验证码输入错误后，密码自动清空，程序自动填充密码框，验证码可重新输入
            try:
                loginElement = driver.find_element_by_id("butn")
            except NoSuchElementException:
                loginElement = None

    # 进入主页面后
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sider___g53Yu")))
    print("cookiesStr = %s" % CookieUtils.getCookiesStr(driver))


def recognize_captcha(driver: WebDriver, imgFilePath, tujian_username=None, tujian_pwd=None):
    # 获取屏幕缩放因子
    devicePixelRatio = driver.execute_script("return window.devicePixelRatio")
    # 识别验证码
    verifyCodeImgElement = driver.find_element_by_id("captcha")
    verify_code_url = verifyCodeImgElement.get_attribute("src")
    for i in range(1):
        verifyCodeImgElement.click()
        verifyCodeImgElement.screenshot(imgFilePath)
        verifyCodeImg = Image.open(imgFilePath)
        w, h = verifyCodeImg.size
        # verifyCodeImg.thumbnail((w / devicePixelRatio, h / devicePixelRatio))
        verifyCodeImg = verifyCodeImg.convert('L')  # 转换模式 L|RGB
        verifyCodeImg = ImageEnhance.Contrast(verifyCodeImg)  # 增强对比度
        verifyCodeImg = verifyCodeImg.enhance(2.0)  # 增加饱和度
        verifyCodeImg.save(imgFilePath)

        verifyCode = tujian_api_helper.img_recognise(tujian_username, tujian_pwd, imgFilePath)
        # verifyCode = ""
        if verifyCode:
            os.rename(imgFilePath,
                      veryeast_config.SCREEN_IMG_DIR + "/" + verifyCode.upper() + "_" + TimeUtils.microsecondStr() + ".png")
        return verifyCode


if __name__ == '__main__':
    login(webdriver.Chrome(), account.tujian_account, account.tujian_pwd)
    os._exit(0)
