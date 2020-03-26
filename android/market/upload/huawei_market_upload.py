import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from android.market.upload.IMarketUpload import IMarketUpload
from android.market.upload.enums import AppName
from base.email import aliyun_email
from base.selenium import ElementUtils


class HuaweiMarketUpload(IMarketUpload):

    def __init__(self, market_channel, app_name, apk_dir_path):
        super().__init__(market_channel, app_name, apk_dir_path)
        width = self.driver.execute_script("return window.screen.availWidth")
        height = self.driver.execute_script("return window.screen.availHeight")
        # 华为市场 应用信息页面 左侧栏 如果浏览器宽度太小 则布局会自动收起左侧菜单栏，点击左箭头，左侧菜单才会弹出
        self.driver.set_window_size(width, height)

    def login(self):
        IMarketUpload.login(self)
        username_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "hwid-cover-input")))
        self.driver.execute_script("arguments[0].value='';", username_input)
        username_input.send_keys(self.account_info[0])
        password_div = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "hwid-password-root")))
        password_input = password_div.find_element_by_class_name("hwid-input")
        self.driver.execute_script("arguments[0].value='';", password_input)
        password_input.send_keys(self.account_info[1])
        time.sleep(0.2)  # 给予 登录按钮 刷新 为可点击状态的缓冲时间
        login_btn = self.driver.find_element_by_class_name("hwid-login-btn")
        login_btn.click()
        time.sleep(2)
        login_btn = ElementUtils.findElement(self.driver, By.CLASS_NAME, "hwid-login-btn")
        if login_btn is not None:
            mobile_captcha_dialog = WebDriverWait(self.driver, 10 * 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "hwid-dialog-main")))
            # 选择其他验证方式
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "textBtn"))).click()
            # 点击 使用邮箱
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "userAccount"))).click()
            # 点击 获取验证码
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "hwid-smsCode"))).click()
            captcha_text = aliyun_email.loginAndGetCaptcha(self.driver, self.account_info[2], self.account_info[3], "华为", "验证码输入框")
            captcha_input = self.driver.find_element_by_class_name("hwid-getAuthCode-input").find_element_by_class_name("hwid-input")
            captcha_input.send_keys(captcha_text)
            confirm_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-next")))
            confirm_btn.click()
            confirm_btn.click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))).click()

    def select_app(self):
        content_iframe = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "fluid-column")))
        self.driver.switch_to.frame(content_iframe)
        app_list_table = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "applist-table")))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "app-version-link")))
        rows = app_list_table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for index, row in enumerate(rows):
            name_element = row.find_element_by_id("ProductListAppDetail%d" % index)
            name = name_element.text.strip()
            if self.app_name == name or (
                    (self.app_name == AppName.mockuai_star_seller or self.app_name == AppName.penguin_shop_seller)
                    and self.app_name in name) or (
                    (self.app_name == AppName.penguin_shop_seller and "无敌掌柜商家" in name)):
                # app_versions = row.find_element_by_class_name("app-type-version-list").find_elements_by_class_name("app-version-link")
                # if len(app_versions) > 1:
                #     app_versions[1].find_element_by_tag_name("a").click()
                # else:
                name_element.click()
                break
        self.driver.switch_to.default_content()

    def upload(self, apk_file, update_msg, is_auto_commit):
        app_info = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "97458334310914199")))
        version_info_second_child_tab = ElementUtils.findElement(self.driver, By.ID, "974583343109141981")
        version_update_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.ID, "VersionButton")))[1]
        if version_info_second_child_tab is None:
            version_update_btn.click()  # 跳转到 新版本 准备提交的tab页面
            app_info.click()  # 点击应用信息 去修改更新文案
        # 应用信息-更新 新版本特性
        time.sleep(1)
        content_iframe = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "mainIframeView")))
        self.driver.switch_to.frame(content_iframe)
        new_version_msg_textarea = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "AppInfoNewFeaturesInputBox")))
        if new_version_msg_textarea.get_attribute("value").strip() != update_msg.strip():
            new_version_msg_textarea.click()
            new_version_msg_textarea.clear()
            # self.driver.execute_script("arguments[0].value='%s';" % update_msg, new_version_msg_textarea)
            new_version_msg_textarea.send_keys(update_msg)
            time.sleep(0.2)
            self.driver.find_element_by_id("AppInfoSaveButtonCn").click()  # 保存
            jump_to_version_info_dialog = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "ngdialog1")))
            jump_to_version_info_dialog.find_element_by_id("CommonConfirmButtonOk").click()  # 确定 取消CommonConfirmButtonClose
            WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located((By.ID, "ngdialog1")))
        else:
            self.driver.switch_to.default_content()
            # 新版本 准备提交
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "974583343109141980"))).click()
        time.sleep(1)
        # 上传apk
        content_iframe = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "mainIframeView")))
        self.driver.switch_to.frame(content_iframe)
        # 软件包管理
        package_manage_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "VerInfoDownloadLink")))
        package_manage_btn.click()
        # 软件包选取和上传弹窗
        packageSelectDialog = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "packageSelectDialog")))
        # 弹窗里的上传按钮
        upload_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "ManageAppUploadPackageButton")))
        self.driver.execute_script("arguments[0].focus();", upload_btn)
        self.driver.execute_script("arguments[0].click();", upload_btn)
        # 上传包弹窗
        upload_apk_dialog = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "spliceUploderContainer")))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "uploader-element-invisible"))).send_keys(apk_file)
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located((By.ID, "spliceUploderContainer")))
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "packageSelectDialog")))
        # 绿色应用申请 点击不申请
        self.driver.find_element_by_id("VerInfoNotApplyButton").click()
        # 发布时间
        self.driver.find_element_by_id("VerInfoReviewImmediateReleaseCheckBox").click()  # 审核通过立即上架
        # 提交审核
        if is_auto_commit:
            self.driver.find_element_by_id("VerInfoSubmitButton").click()




