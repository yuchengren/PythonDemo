import json
import os
from io import BytesIO
import requests

from selenium.common.exceptions import NoSuchElementException
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import base.config.account
from veryeast.config import veryeast_config
from PIL import Image, ImageEnhance
import pytesseract
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def recognize_captcha(img_file):
    file_name = os.path.basename(img_file)
    with open(img_file, "rb") as f:
        content = f.read()

        # 识别
    s = time.time()
    url = "http://127.0.0.1:6000/b"
    files = {'image_file': (file_name, BytesIO(content), 'application')}
    r = requests.post(url=url, files=files)
    return json.loads(r.text)["value"]


def captchaScreenShot(driver: WebDriver, imgFilePath, devicePixelRatio):
    # 识别验证码
    # 获取验证码位置信息
    verifyCodeImgElement = driver.find_element_by_id("captcha")
    verifyCodeImgLocation = verifyCodeImgElement.location
    verifyCodeImgSize = verifyCodeImgElement.size
    verifyCodeImgLeft = verifyCodeImgLocation['x']
    verifyCodeImgTop = verifyCodeImgLocation['y']
    verifyCodeImgRight = verifyCodeImgLeft + verifyCodeImgSize['width']
    verifyCodeImgBottom = verifyCodeImgTop + verifyCodeImgSize['height']
    # 登录页面全屏截图
    driver.get_screenshot_as_file(imgFilePath)
    # 从全屏截图 截取验证码区域
    verifyCodeImg = Image.open(imgFilePath).crop((verifyCodeImgLeft * devicePixelRatio,
                                                  verifyCodeImgTop * devicePixelRatio,
                                                  verifyCodeImgRight * devicePixelRatio,
                                                  verifyCodeImgBottom * devicePixelRatio))
    verifyCodeImg = verifyCodeImg.convert('L')  # 转换模式 L|RGB
    verifyCodeImg = ImageEnhance.Contrast(verifyCodeImg)  # 增强对比度
    verifyCodeImg = verifyCodeImg.enhance(2.0)  # 增加饱和度

    verifyCodeImg = verifyCodeImg.resize((int(verifyCodeImgSize['width']),
                                         int(verifyCodeImgSize['height'])))  # 缩放至原图大小
    verifyCodeImg.save(imgFilePath)
    # time.sleep(0.5)


def inputPwdCaptchaAndLogin(driver: WebDriver, imgFilePath, devicePixelRatio):
    captchaScreenShot(driver, imgFilePath, devicePixelRatio)
    # 输入密码
    inputPasswordElement = driver.find_element_by_id("password")
    inputPasswordElement.send_keys(base.config.account.veryeast_pwd)
    verifyCode = recognize_captcha(imgFilePath)
    print("recognize verifyCode = %s" % verifyCode)
    # 输入验证码
    verifyCodeElement = driver.find_element_by_id("Txtidcode")
    verifyCodeElement.send_keys(verifyCode)

    # 点击登录
    loginElement = driver.find_element_by_id("butn")
    loginElement.click()
    time.sleep(1)

    try:
        loginElement = driver.find_element_by_id("butn")
    except NoSuchElementException:
        loginElement = None
    return loginElement


def login(driver: WebDriver):
    imgFilePath = veryeast_config.SCREEN_IMG_DIR + "/img.png"

    # 打开后台网址
    driver.get(veryeast.config.veryeast_config.BG_SYSTEM_URL)
    # 获取屏幕缩放因子
    devicePixelRatio = driver.execute_script("return window.devicePixelRatio")
    print("devicePixelRatio=%s" % devicePixelRatio)

    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    print("width=%s, height=%s" % (width, height))
    driver.set_window_size(width, height)
    # 输入用户名
    inputUserNameElement = driver.find_element_by_id("username")
    inputUserNameElement.send_keys(base.config.account.veryeast_username)

    loginElement = driver.find_element_by_id("butn")
    while loginElement is not None:
        loginElement = inputPwdCaptchaAndLogin(driver, imgFilePath, devicePixelRatio)

    # 进入主页面后
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "sider___g53Yu")))

