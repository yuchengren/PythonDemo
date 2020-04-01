import os
import threading
import traceback
import zipfile

from android.market.config import market_config
from android.market.upload.enums import MarketChannel, AppName
from android.market.upload.huawei_market_upload import HuaweiMarketUpload
from android.market.upload.oppo_market_upload import OppoMarketUpload
from android.market.upload.tencent_market_upload import TencentMarketUpload
from android.market.upload.vivo_market_upload import VivoMarketUpload
from android.market.upload.xiaomi_market_upload import XiaomiMarketUpload
from base.utils import FileUtils, TimeUtils

"""
需要手动输入验证码的地方：
oppo登录页面、登录阿里云邮箱页面
vivo登录页面
huawei登录页面、登录阿里云邮箱页面
"""


# 应用市场脚本执行的行为类型
class MarketActionType:
    login = 1  # 登录
    goto_applist_page = 2  # 登录后跳转app列表页面
    select_app = 3  # 跳转app列表页面后，选择需要更新的app
    upload = 4  # 在选择的app更新页面，上传新apk


# app类型
app_name = AppName.mockuai_star_buyer
# apk更新日志
update_msg = "【优化】\n修复已知问题，优化用户体验\n更多细节优化，立即下载体验吧~"

market_list = [
    # MarketChannel.xiaomi,
    # MarketChannel.oppo,
    # MarketChannel.vivo,
    # MarketChannel.tencent,
    MarketChannel.huawei,
]
isAutoCommit = False  # 最后一步 是否自动提交 建议设为False 人为核对信息后 再手动点击提交
isCheckChannelApkZipToday = True  # 是否校验渠道apk压缩包是否是今天的
market_action_type = MarketActionType.upload


def unzipChannelApkZip():
    apkDirPath = ""
    files = os.listdir(market_config.apk_zip_parent_path)
    for f in files:
        file_path = os.path.join(market_config.apk_zip_parent_path, f)
        base_name = os.path.basename(f)
        modify_time = os.path.getmtime(file_path)
        if base_name == market_config.apk_zip_name and (TimeUtils.isToday(modify_time) or not isCheckChannelApkZipToday):
            zip_files = zipfile.ZipFile(os.path.join(market_config.apk_zip_parent_path, f))
            apk_dir = os.path.join(market_config.apk_zip_parent_path, market_config.apk_dir_name)
            if os.path.exists(apk_dir):
                FileUtils.deleteFile(apk_dir)
            else:
                os.makedirs(apk_dir)
            for apk_name in zip_files.namelist():
                zip_files.extract(apk_name, market_config.apk_zip_parent_path)
            zip_files.close()
            apkDirPath = os.path.join(market_config.apk_zip_parent_path, market_config.apk_dir_name)
            break
    return apkDirPath


def get_market_upload_obj(market_channel, _app_name, _apk_dir_path):
    marketUploadObj = None
    if market_channel == MarketChannel.xiaomi:
        marketUploadObj = XiaomiMarketUpload(market_channel, _app_name, apk_dir_path)
    elif market_channel == MarketChannel.oppo:
        marketUploadObj = OppoMarketUpload(market_channel, _app_name, apk_dir_path)
    elif market_channel == MarketChannel.vivo:
        marketUploadObj = VivoMarketUpload(market_channel, _app_name, apk_dir_path)
    elif market_channel == MarketChannel.tencent:
        marketUploadObj = TencentMarketUpload(market_channel, _app_name, apk_dir_path)
    elif market_channel == MarketChannel.huawei:
        marketUploadObj = HuaweiMarketUpload(market_channel, _app_name, apk_dir_path)
    return marketUploadObj


def execute(market_channel, _app_name, _apk_dir_path):
    apk_file = ""
    marketUploadObj = get_market_upload_obj(market_channel, _app_name, _apk_dir_path)
    if marketUploadObj is None:
        return
    if market_action_type >= MarketActionType.login:
        marketUploadObj.login()
    if market_action_type >= MarketActionType.goto_applist_page:
        marketUploadObj.goto_app_list_page()
    if market_action_type >= MarketActionType.select_app:
        marketUploadObj.select_app()
    if market_action_type >= MarketActionType.upload:
        apk_file = marketUploadObj.findMarketApkFile(_apk_dir_path)
        if len(apk_file) == 0:
            raise Exception("_app_name = %s market_channel = %s, cannot find the apk file in %s" %
                            (_app_name, market_channel, _apk_dir_path))
        marketUploadObj.upload(apk_file, update_msg, isAutoCommit)
    print("driver execute end,_app_type = %s, market_channel = %s, apk_file = %s" %
          (_app_name, market_channel, apk_file))


apk_dir_path = ""
if market_action_type >= MarketActionType.upload:
    apk_dir_path = unzipChannelApkZip()
    if len(apk_dir_path) == 0:
        raise Exception("can not find apk zip and do unzip")
thread_list = []
for market in market_list:
    try:
        thread = threading.Thread(target=execute, args=(market, app_name, apk_dir_path))
        thread.start()
        thread_list.append(thread)
    except Exception as e:
        print("upload %s %s occur exception:" % (app_name, market))
        traceback.print_exc()

for t in thread_list:
    t.join()  # 线程A中使用B.join()表示线程A在调用join()处被阻塞，且要等待线程B的完成才能继续执行

os._exit(1)  # 防止程序执行完后，浏览器被自动关闭




