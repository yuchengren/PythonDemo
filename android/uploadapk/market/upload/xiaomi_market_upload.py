from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from android.uploadapk.market.upload.IMarketUpload import IMarketUpload


class XiaomiMarketUpload(IMarketUpload):

    def __init__(self, market_channel, app_name, apk_dir_path):
        super().__init__(market_channel, app_name, apk_dir_path)

    def login(self):
        IMarketUpload.login(self)
        login_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "btnadpt")))
        self.driver.find_element_by_id("username").send_keys(self.account_info[0])
        self.driver.find_element_by_id("pwd").send_keys(self.account_info[1])
        login_btn.click()

    def select_app(self):
        app_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "game-list")))
        apps = app_list.find_elements_by_class_name("list-item")
        for app in apps:
            if self.app_name == app.find_element_by_class_name("game-name").text.strip():
                update_app_version = app.find_element_by_class_name("games-operate").find_elements_by_class_name("btn")[0]
                if "myicon-edit" in update_app_version.get_attribute("class"):
                    self.is_editing = True
                update_app_version.click()
                break

    def upload(self, apk_file, update_msg, is_auto_commit):
        if self.is_editing:  # 如果处于上次保存的编辑状态，则重新上传apk，防止上次上传的apk不是最新的
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "toolbar-upload"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "uploadMainBtn")))  # 点击上传按钮
        self.driver.find_element_by_tag_name("input").send_keys(apk_file)
        # 上传进度
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "progress-bar")))
        WebDriverWait(self.driver, self.upload_time_check).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "progress-bar")))
        # 完善资料页面外层
        choose_timed = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "choose_timed")))
        Select(choose_timed).select_by_value("notimed")  # 审核通过后立即上线
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "submit"))).click()
        # 点击填写资料
        write_info = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "J_fillInfo")))
        write_info.find_element_by_class_name("ChooseLanguageBtn").click()
        # 更新资料页面-更新日志
        update_msg_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "changeLog")))
        self.driver.execute_script("arguments[0].value='';", update_msg_input)
        update_msg_input.send_keys(update_msg)
        self.driver.find_element_by_id("submit").click()
        # 完善资料外层页面
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "J_upInfo")))
        if is_auto_commit:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "submit"))).click()
