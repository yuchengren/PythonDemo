import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from android.market.upload.IMarketUpload import IMarketUpload
from android.market.upload.enums import AppName
from base.selenium import ElementUtils


class VivoMarketUpload(IMarketUpload):

    def __init__(self, market_channel, app_name, apk_dir_path):
        super().__init__(market_channel, app_name, apk_dir_path)

    def login(self):
        IMarketUpload.login(self)
        username_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "name")))
        username_input.send_keys(self.account_info[0])
        login_btn = self.driver.find_element_by_class_name("btn-event")
        while login_btn is not None:
            login_btn = self.input_password_and_captcha(self.driver, self.account_info[1])

    @staticmethod
    def input_password_and_captcha(_driver: WebDriver, password):
        captcha_elements = ElementUtils.findElements(_driver, By.NAME, "verificationCode")
        login_btn = ElementUtils.findElement(_driver, By.CLASS_NAME, "btn-event")
        inputPasswordElement = _driver.find_element_by_name("password")
        if len(inputPasswordElement.get_attribute('value').strip()) == 0:
            inputPasswordElement.send_keys(password)
            captcha_elements = ElementUtils.findElements(_driver, By.NAME, "verificationCode")
            if captcha_elements is not None and len(captcha_elements) > 1:
                _driver.execute_script("arguments[0].focus();", captcha_elements[1])
        time.sleep(5)
        if len(captcha_elements[1].get_attribute('value').strip()) == 4:
            login_btn.click()
            # class "fadeInDown" "fadeOutUp"  id walleUtilLoading
            # WebDriverWait(_driver, 10).until_not(EC.visibility_of_element_located((By.ID, "walleUtilLoading")))
            time.sleep(2)
            login_btn = ElementUtils.findElement(_driver, By.CLASS_NAME, "btn-event")
        return login_btn

    def goto_app_list_page(self):
        # 管理中心按钮
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "manage-warp"))).click()
        time.sleep(0.2)
        dialog_remind = ElementUtils.findElement(self.driver, By.CLASS_NAME, "el-dialog--center")
        if dialog_remind is not None:
            webdriver.ActionChains(self.driver).send_keys(
                Keys.ESCAPE).perform()  # 管理中心的通知弹窗 esc 等效于关闭按钮(class="el-button")
            WebDriverWait(self.driver, 10).until_not(
                EC.visibility_of_element_located((By.CLASS_NAME, "el-dialog--center")))
        app_and_game = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="page-template"]/div[2]/div[3]/ul/li[1]')))
        self.driver.execute_script("arguments[0].click();", app_and_game)

    def select_app(self):
        app_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "el-table__body-wrapper")))
        app_rows = app_list.find_elements_by_class_name("el-table__row")
        for row in app_rows:
            name = row.find_elements_by_tag_name("td")[1].text.strip()
            if self.app_name == name or (
                    (self.app_name == AppName.mockuai_star_seller or self.app_name == AppName.penguin_shop_seller)
                    and self.app_name in name):
                row.click()
                break
        # 点击版本升级
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "el-button--warning"))).click()

    def upload(self, apk_file, update_msg, is_auto_commit):
        apk_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "el-upload__input")))
        apk_input.send_keys(apk_file)
        # 新版说明
        update_msg_input = self.driver.find_elements_by_class_name("el-textarea__inner")[1]
        self.driver.execute_script("arguments[0].value='';", update_msg_input)
        update_msg_input.send_keys(update_msg)
        # 发布时间 审核通过后立即发布
        self.driver.find_elements_by_class_name("el-radio__input")[0].click()
        # 上传进度
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "el-progress-bar")))
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "el-progress-bar")))
        # 提交
        if is_auto_commit:
            self.driver.find_element_by_class_name("button-wrap").find_element_by_class_name("el-button--primary").click()