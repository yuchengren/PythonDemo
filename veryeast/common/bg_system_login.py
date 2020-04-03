from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

import veryeast.config.veryeast_info
from base.selenium import CookieUtils
from veryeast.config import veryeast_config
from PIL import Image, ImageEnhance
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver: WebDriver):
    imgFilePath = veryeast_config.SCREEN_IMG_DIR + "/img.png"

    # 打开后台网址
    driver.get(veryeast.config.veryeast_info.BG_SYSTEM_URL)
    # 获取屏幕缩放因子
    devicePixelRatio = driver.execute_script("return window.devicePixelRatio")
    print("devicePixelRatio=%s" % devicePixelRatio)

    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    print("width=%s, height=%s" % (width, height))
    driver.set_window_size(width, height)
    # 输入用户名
    inputUserNameElement = driver.find_element_by_id("username")
    inputUserNameElement.send_keys(veryeast.config.veryeast_info.USER_NAME)
    # 输入密码
    inputPasswordElement = driver.find_element_by_id("password")
    inputPasswordElement.send_keys(veryeast.config.veryeast_info.PASSWORD)

    # 识别验证码
    # 获取验证码位置信息
    verifyCodeImgElement = driver.find_element_by_id("captcha")
    verifyCodeImgLocation = verifyCodeImgElement.location
    verifyCodeImgSize = verifyCodeImgElement.size
    verifyCodeImgLeft = verifyCodeImgLocation['x']
    verifyCodeImgTop = verifyCodeImgLocation['y']
    verifyCodeImgRight = verifyCodeImgLeft + verifyCodeImgSize['width']
    verifyCodeImgBottom = verifyCodeImgTop + verifyCodeImgSize['height']

    print((verifyCodeImgLeft, verifyCodeImgTop, verifyCodeImgRight, verifyCodeImgBottom))
    # 登录页面全屏截图
    # driver.get_screenshot_as_file(imgFilePath)
    # 从全屏截图 截取验证码区域
    verifyCodeImg = Image.open(imgFilePath).crop((verifyCodeImgLeft * devicePixelRatio,
                                                  verifyCodeImgTop * devicePixelRatio,
                                                  verifyCodeImgRight * devicePixelRatio,
                                                  verifyCodeImgBottom * devicePixelRatio))
    verifyCodeImg = verifyCodeImg.convert('L')  # 转换模式 L|RGB
    verifyCodeImg = ImageEnhance.Contrast(verifyCodeImg)  # 增强对比度
    verifyCodeImg = verifyCodeImg.enhance(2.0)  # 增加饱和度
    # verifyCodeImg.save(imgFilePath)
    # time.sleep(0.5)
    verifyCode = ""
    print("verifyCode = %s" % verifyCode)

    # 输入验证码
    verifyCodeElement = driver.find_element_by_id("Txtidcode")
    verifyCodeElement.send_keys(verifyCode)

    verifyCodeValue = verifyCodeElement.get_attribute('value').strip()
    print("verifyCodeValue = %s" % verifyCodeValue)
    while len(verifyCodeValue) != 4:
        time.sleep(5)
        verifyCodeValue = verifyCodeElement.get_attribute('value').strip()

    # 点击登录
    loginElement = driver.find_element_by_id("butn")
    loginElement.click()
    time.sleep(1)

    # 验证码输入错误后，密码自动清空，程序自动填充密码框，验证码可重新输入
    try:
        loginElement = driver.find_element_by_id("butn")
    except NoSuchElementException:
        loginElement = None

    while loginElement is not None:
        inputPasswordElement = driver.find_element_by_id("password")
        if len(inputPasswordElement.get_attribute('value').strip()) == 0:
            inputPasswordElement.send_keys(veryeast.config.veryeast_info.PASSWORD)
            verifyCodeElement = driver.find_element_by_id("Txtidcode")
            driver.execute_script("arguments[0].focus();", verifyCodeElement)
        time.sleep(5)
        if len(verifyCodeElement.get_attribute('value').strip()) == 4:
            loginElement.click()
            time.sleep(1)
            try:
                loginElement = driver.find_element_by_id("butn")
            except NoSuchElementException:
                loginElement = None

    # 进入主页面后
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "sider___g53Yu")))
    print("cookiesStr = %s" % CookieUtils.getCookiesStr(driver))


if __name__ == '__main__':
    login(webdriver.Firefox())
