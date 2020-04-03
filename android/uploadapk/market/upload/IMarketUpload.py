import os

from selenium import webdriver

from android.uploadapk.market.config import mockuai_config, haoyina_config, market_urls
from android.uploadapk.market.upload.enums import AppName, MarketChannel


class IMarketUpload:

    def __init__(self, market_channel, app_name, apk_dir_path):
        self.upload_time_check = 60
        self.market_channel = market_channel
        self.app_name = app_name
        self.apk_dir_path = apk_dir_path
        self.is_editing = False
        self.account_info = self.getAccountInfo()
        # 浏览器
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        pass

    def login(self):
        self.driver.get(self.getMarketUrl())

    def goto_app_list_page(self):
        pass

    def select_app(self):
        raise Exception('')

    def upload(self, apk_file, update_msg, is_auto_commit):
        raise Exception('')

    def findMarketApkFile(self, parent_path):
        apkPath = ""
        files = os.listdir(parent_path)
        for f in files:
            base_name = os.path.basename(f)
            if self.market_channel in base_name and base_name.endswith(".apk"):
                apkPath = os.path.join(parent_path, f)
        return apkPath

    def getMarketUrl(self):
        market_url = ""
        if self.market_channel == MarketChannel.xiaomi:
            market_url = market_urls.xiaomi_market_apps_page
        elif self.market_channel == MarketChannel.oppo:
            market_url = market_urls.oppo_market_apps_page
        elif self.market_channel == MarketChannel.vivo:
            market_url = market_urls.vivo_market_apps_page
        elif self.market_channel == MarketChannel.tencent:
            market_url = market_urls.tencent_market_apps_page
        elif self.market_channel == MarketChannel.huawei:
            market_url = market_urls.huawei_market_apps_page
        return market_url

    def getAccountInfo(self):
        account_info = []
        if self.app_name == AppName.wudi_zhubo_seller:
            if self.market_channel == MarketChannel.xiaomi:
                account_info = [haoyina_config.xiaomi_market_username, haoyina_config.xiaomi_market_password]
            elif self.market_channel == MarketChannel.oppo:
                account_info = [haoyina_config.oppo_market_username, haoyina_config.oppo_market_password
                                , haoyina_config.aliyun_email_username, haoyina_config.aliyun_email_password]
            elif self.market_channel == MarketChannel.vivo:
                account_info = [haoyina_config.vivo_market_username, haoyina_config.vivo_market_password]
            elif self.market_channel == MarketChannel.tencent:
                account_info = [haoyina_config.tencent_market_username, haoyina_config.tencent_market_password]
            elif self.market_channel == MarketChannel.huawei:
                account_info = [haoyina_config.huawei_market_username, haoyina_config.huawei_market_password
                                , haoyina_config.aliyun_email_username, haoyina_config.aliyun_email_password]
        else:
            if self.market_channel == MarketChannel.xiaomi:
                account_info = [mockuai_config.xiaomi_market_username, mockuai_config.xiaomi_market_password]
            elif self.market_channel == MarketChannel.oppo:
                account_info = [mockuai_config.oppo_market_username, mockuai_config.oppo_market_password
                                , mockuai_config.oppo_market_username, mockuai_config.oppo_market_password]
            elif self.market_channel == MarketChannel.vivo:
                account_info = [mockuai_config.vivo_market_username, mockuai_config.vivo_market_password]
            elif self.market_channel == MarketChannel.tencent:
                account_info = [mockuai_config.tencent_market_username, mockuai_config.tencent_market_password]
            elif self.market_channel == MarketChannel.huawei:
                account_info = [mockuai_config.huawei_market_username, mockuai_config.huawei_market_password
                                , mockuai_config.aliyun_email_username, mockuai_config.aliyun_email_password]
        return account_info
