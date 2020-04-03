import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from android.uploadapk.market.upload.IMarketUpload import IMarketUpload
from base.email import aliyun_email


class OppoMarketUpload(IMarketUpload):

    def __init__(self, market_channel, app_name, apk_dir_path):
        super().__init__(market_channel, app_name, apk_dir_path)

    def login(self):
        IMarketUpload.login(self)
        login_way = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "tabloginway")))
        login_way.find_elements_by_tag_name("p")[1].click()  # 密码登录
        username_input = self.driver.find_element_by_class_name("account").find_element_by_tag_name("input")
        self.driver.execute_script("arguments[0].value='';", username_input)
        username_input.send_keys(self.account_info[0])
        password_div = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "password")))
        password_div.find_element_by_tag_name("input").send_keys(self.account_info[1])
        login_btn = self.driver.find_element_by_class_name("passlogin").find_element_by_class_name("primary_btn")
        login_btn.click()
        # 可能会弹出 图形拖动型验证码
        while "index" in self.driver.current_url:
            time.sleep(1)
        current_url = self.driver.current_url
        # 弹出手机验证码输入框 网站未自动发出验证码
        if "once_verification" in current_url:
            change_verify_way_el = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "detail_small")))
            change_verify_way_el.find_element_by_tag_name("span").click()
            list_contents = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list_content")))
            list_contents[1].click()
        # 弹出邮箱验证码输入框 网站已自动发出验证码
        if "verification" in self.driver.current_url:
            email_code_div = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "emailcode")))
            email_code_input = email_code_div.find_element_by_tag_name("input")
            email_code_input.send_keys(aliyun_email.loginAndGetCaptcha(self.driver, self.account_info[2], self.account_info[3], "OPPO", "验证码"))
            self.driver.find_element_by_class_name("primary_btn").click()

    def select_app(self):
        app_list_table = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "table")))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "update")))
        rows = app_list_table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for row in rows:
            if self.app_name == row.find_element_by_class_name("appname").text.strip():
                update_btn = row.find_element_by_class_name("update")
                # 直接click,报selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted
                # 可能是因为 回到顶部的浮动窗口 遮挡住
                self.driver.execute_script("arguments[0].click();", update_btn)
                break

    def upload(self, apk_file, update_msg, is_auto_commit):
        # 上传apk
        apk_uploader_wrap = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "apk-uploader-wrap")))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "file-ipt")))
        apk_uploader_wrap.find_element_by_class_name("file-ipt").send_keys(apk_file)
        # 更新日志
        update_desc = self.driver.find_element_by_name("update_desc")
        self.driver.execute_script("arguments[0].value='';", update_desc)
        update_desc.send_keys(update_msg)
        # 发布时间
        self.driver.find_element_by_class_name("sche-online-time-on").click()  # 审核后立即发布
        # 上传进度
        time.sleep(0.2)
        upload_text = self.driver.find_element_by_class_name("apk-uploader").find_element_by_class_name("btn-text")
        while "%" in upload_text.text or "解析" in upload_text.text:
            time.sleep(0.5)
        # 提交审核
        if is_auto_commit:
            self.driver.find_element_by_id("auditbutton").click()




