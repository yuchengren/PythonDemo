import os

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver

from base.api import tujian_api_helper
from base.config import account, char_set, configs
from base.selenium import CookieUtils
from base.tensorflow.recognition_object import Recognizer
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

    width = driver.execute_script("return window.screen.height")
    height = driver.execute_script("return window.screen.width")
    # print("driver width=%d height=%d" % (width, height))
    driver.set_window_size(1366, 768)
    # 获取屏幕缩放因子
    devicePixelRatio = driver.execute_script("return window.devicePixelRatio")
    print("devicePixelRatio = %d" % devicePixelRatio)
    # 输入用户名
    inputUserNameElement = driver.find_element_by_id("username")
    inputUserNameElement.send_keys(username)

    auto_recognise_count = 0
    loginElement = driver.find_element_by_id("butn")
    recognised_img_path = ""
    while loginElement is not None:
        if auto_recognise_count >= AUTO_RECOGNISE_MAX_COUNT:
            raise Exception("auto recognise captcha fail over %d " % AUTO_RECOGNISE_MAX_COUNT)
        inputPasswordElement = driver.find_element_by_id("password")
        verifyCodeElement = driver.find_element_by_id("Txtidcode")
        if len(inputPasswordElement.get_attribute('value').strip()) == 0:
            inputPasswordElement.send_keys(pwd)
            if not is_auto_recognise:
                driver.execute_script("arguments[0].focus();", verifyCodeElement)
        if is_auto_recognise:
            verifyCode_list = recognize_captcha(driver, devicePixelRatio, imgFilePath, tujian_username, tujian_pwd)
            recognised_img_path = verifyCode_list[1]
            auto_recognise_count += 1
            verifyCodeElement.send_keys(verifyCode_list[0])
        else:
            time.sleep(5)
        if len(verifyCodeElement.get_attribute('value').strip()) == 4:
            loginElement.click()
            time.sleep(1)
            # 验证码输入错误后，密码自动清空，程序自动填充密码框，验证码可重新输入
            try:
                loginElement = driver.find_element_by_id("butn")
                # 把识别错误的验证码移到错误验证码文件夹
                if os.path.exists(recognised_img_path):
                    recognised_img_path_error = veryeast_config.SCREEN_IMG_ERROR_DIR + "/" + os.path.basename(recognised_img_path)
                    print("recognise success,count=%d,img_path=%s" % (auto_recognise_count, recognised_img_path_error))
                    os.rename(recognised_img_path, recognised_img_path_error)
            except NoSuchElementException:
                print("recognise success,count=%d,img_path=%s" % (auto_recognise_count, recognised_img_path))
                loginElement = None

    # 进入主页面后
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sider___g53Yu")))
    print("cookiesStr = %s" % CookieUtils.getCookiesStr(driver))


def recognize_captcha(driver: WebDriver, devicePixelRatio, imgFilePath, tujian_username=None, tujian_pwd=None):
    # 识别验证码
    verifyCodeImgElement = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "captcha")))
    # verify_code_url = verifyCodeImgElement.get_attribute("src")
    verifyCodeImgElement.screenshot(imgFilePath)
    verifyCodeImg = Image.open(imgFilePath)
    if type(driver) is selenium.webdriver.firefox.webdriver.WebDriver:
        w, h = verifyCodeImg.size
        verifyCodeImg.thumbnail((w / devicePixelRatio, h / devicePixelRatio))
    verifyCodeImg = verifyCodeImg.convert('L')  # 转换模式 L|RGB
    verifyCodeImg = ImageEnhance.Contrast(verifyCodeImg)  # 增强对比度
    verifyCodeImg = verifyCodeImg.enhance(2.0)  # 增加饱和度
    verifyCodeImg.save(imgFilePath)

    # verifyCode = tujian_api_helper.img_recognise(tujian_username, tujian_pwd, imgFilePath)
    verifyCode = tensorflow_recognize(imgFilePath)
    new_image_path = veryeast_config.SCREEN_IMG_DIR + "/" + verifyCode.upper() + "_" + TimeUtils.microsecondStr() + ".png"
    if verifyCode:
        os.rename(imgFilePath, new_image_path)
    return [verifyCode, new_image_path]


def tensorflow_recognize(imgFilePath):
    R = Recognizer(48, 117, 4, char_set.number_upper_letter, configs.MODELS_DIR + "/model_veryeast/")
    r_img = Image.open(imgFilePath)
    return R.rec_image(r_img)


if __name__ == '__main__':
    login(webdriver.Firefox(), account.veryeast_username, account.veryeast_pwd,  account.tujian_account, account.tujian_pwd)
    os._exit(1)
