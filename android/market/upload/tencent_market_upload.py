import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from android.market.upload.IMarketUpload import IMarketUpload
from android.market.upload.enums import AppName
from base.selenium import ElementUtils


class TencentMarketUpload(IMarketUpload):

    def __init__(self, market_channel, app_name, apk_dir_path):
        super().__init__(market_channel, app_name, apk_dir_path)

    def login(self):
        IMarketUpload.login(self)
        login_iframe = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "login_frame")))
        self.driver.switch_to.frame(login_iframe)
        login_by_account = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "switcher_plogin")))
        login_by_account.click()  # 账号密码登录
        username_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "u")))
        self.driver.execute_script("arguments[0].value='';", username_input)
        username_input.send_keys(self.account_info[0])
        password_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "p")))
        self.driver.execute_script("arguments[0].value='';", password_input)
        password_input.send_keys(self.account_info[1])
        self.driver.find_element_by_id("login_button").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "loading_tips")))
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located((By.ID, "loading_tips")))
        time.sleep(0.2)

    def goto_app_list_page(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "update-apk")))
        guide = ElementUtils.findElement(self.driver, By.ID, "j-guide-box")
        if guide is not None:
            guide.click()
            WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located((By.ID, "j-guide-box")))

    def select_app(self):
        app_list_table = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "table-app-list")))
        rows = app_list_table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for row in rows:
            name = row.find_element_by_class_name("app-name").text.strip()
            if self.app_name == name or (
                    (self.app_name == AppName.mockuai_star_seller or self.app_name == AppName.penguin_shop_seller)
                    and self.app_name in name):
                update_btn = row.find_element_by_class_name("update-apk")
                update_btn.click()
                time.sleep(0.1)
                current_window = self.driver.current_window_handle
                for handle in self.driver.window_handles:
                    if handle != current_window:
                        self.driver.switch_to.window(handle)
                        break
                break

    def upload(self, apk_file, update_msg, is_auto_commit):
        # 上传apk
        apk_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "webuploader-element-invisible")))
        apk_input.send_keys(apk_file)
        # 更新日志
        update_desc = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "update_des")))
        self.driver.execute_script("arguments[0].value='';", update_desc)
        update_desc.send_keys(update_msg)
        # 发布时间
        self.driver.find_elements_by_class_name("ui-radio")[2].click()  # 审核后立即发布
        # 上传进度
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "webuploader-container-hide")))
        WebDriverWait(self.driver, self.upload_time_check).until_not(EC.presence_of_element_located((By.CLASS_NAME, "webuploader-container-hide")))
        # 提交审核
        if is_auto_commit:
            self.driver.find_element_by_id("j-submit-btn").click()




