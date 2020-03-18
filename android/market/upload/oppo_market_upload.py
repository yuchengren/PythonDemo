import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from android.market.config import market_urls, market_accounts, market_config
from android.market.upload.IMarketUpload import IMarketUpload
from android.market.upload.enums import AppType


class OppoMarketUpload(IMarketUpload):

    def __init__(self, market_channel, app_name, apk_dir_path):
        super().__init__(market_channel, app_name, apk_dir_path)

    def login(self):
        self.driver.get(market_urls.oppo_market_apps_page)
        login_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "btnadpt")))
        self.driver.find_element_by_id("username").send_keys(market_accounts.oppo_market_username)
        self.driver.find_element_by_id("pwd").send_keys(market_accounts.oppo_market_password)
        # login_btn.click()

    def select_app(self):
        app_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "game-list")))

    def upload(self, apk_file, update_msg, is_auto_commit):
        pass

