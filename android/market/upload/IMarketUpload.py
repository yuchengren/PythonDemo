import os
import zipfile

from selenium import webdriver

from android.market.config import market_config
from android.market.upload.enums import AppType
from base.utils import TimeUtils, FileUtils


class IMarketUpload:

    def __init__(self, market_channel, app_name, apk_dir_path):
        self.market_channel = market_channel
        self.app_name = app_name
        self.apk_dir_path = apk_dir_path
        self.is_editing = False
        # 浏览器
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        pass

    def login(self):
        raise Exception('')

    def select_app(self):
        raise Exception('')

    def upload(self, apk_file, update_msg, is_auto_commit):
        raise Exception('')

    def findMarketApkFile(self, parent_path):
        apkPath = ""
        files = os.listdir(parent_path)
        for f in files:
            base_name = os.path.basename(f)
            if self.market_channel.value in base_name and base_name.endswith(".apk"):
                apkPath = os.path.join(parent_path, f)
        return apkPath

    def findLocalApkFile(self):
        apkPath = ""
        files = os.listdir(market_config.apk_zip_parent_path)
        for f in files:
            file_path = os.path.join(market_config.apk_zip_parent_path, f)
            base_name = os.path.basename(f)
            modify_time = os.path.getmtime(file_path)
            if base_name == market_config.apk_dir_name and os.path.isdir(file_path) and TimeUtils.isToday(modify_time):
                apkPath = self.findMarketApkFile(os.path.join(market_config.apk_zip_parent_path, market_config.apk_dir_name))
                if len(apkPath) != 0:
                    return apkPath
            elif base_name == market_config.apk_zip_name and TimeUtils.isToday(modify_time):
                zip_files = zipfile.ZipFile(os.path.join(market_config.apk_zip_parent_path, f))
                apk_dir = os.path.join(market_config.apk_zip_parent_path, market_config.apk_dir_name)
                if os.path.exists(apk_dir):
                    FileUtils.deleteFile(apk_dir)
                else:
                    os.makedirs(apk_dir)
                for apk_name in zip_files.namelist():
                    zip_files.extract(apk_name, market_config.apk_zip_parent_path)
                zip_files.close()
                return self.findMarketApkFile(os.path.join(market_config.apk_zip_parent_path, market_config.apk_dir_name))
        return apkPath


