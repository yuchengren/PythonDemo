# coding: utf-8
import os
import json
import shutil
import sys
import qrcode

# fix 中文乱码
reload(sys)
sys.setdefaultencoding('utf-8')


def getJobApkFile():
    flavor_name = os.environ["FLAVOR"].lower()
    build_type_name = os.environ["BUILD_TYPE"].lower()
    buildPath = os.environ["WORKSPACE"] + "/app/build"

    is_jiagu = os.environ["jiagu"] == "true"
    is_channel = os.environ["channel"] == "true"
    if is_jiagu and is_channel:
        apkPath = buildPath + "/rebuildChannel"
    elif is_jiagu:
        apkPath = buildPath + "/jiagu"
    else:
        apkPath = os.environ["WORKSPACE"] + "/app/build/outputs/apk/" + flavor_name + "/" + build_type_name

    apkPathFiles = os.listdir(apkPath)
    for file in apkPathFiles:
        if os.path.isfile(os.path.join(apkPath, file)) and os.path.basename(file).endswith(".apk"):
            if is_jiagu:
                if "mockuai" in os.path.basename(file):
                    jobApkFile = os.path.join(apkPath, file)
                    break
            else:
                jobApkFile = os.path.join(apkPath, file)
                break
    if 'uploadApkFile' not in locals().keys():
        jobApkFile = os.path.join(apkPath, apkPathFiles[0])

    return jobApkFile


def deleteOldestFile(path, maxCount):
    fileNames = os.listdir(path)
    if (len(fileNames) <= maxCount) | (maxCount == 0):
        return

    oldestFile = path + fileNames[0]
    oldestTime = os.path.getmtime(oldestFile)
    for fileName in fileNames:
        file = path + fileName
        fileMTime = os.path.getmtime(file)
        if fileMTime < oldestTime:
            oldestFile = file
            oldestTime = fileMTime

    os.remove(oldestFile)


def makeQRCodeImg(data, qrcodeImgFile):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=20
    )
    qr.add_data(data)
    qr.make(fit=True)
    qrcodeImg = qr.make_image()
    qrcodeImg.save(qrcodeImgFile)


def send_appQRCodeURL_to_dingtalk():
    commitStream = os.popen("git log --date=format:\"%Y-%m-%d %H:%M\" --pretty=format:\"commit by %an on %cd\" -n \"1\" ")
    commit = commitStream.read()
    commitStream.close()
    print commit

    msgStream = os.popen("git log --pretty=format:\"%s\" -n \"1\" ")
    msg = msgStream.read()
    msgStream.close()
    print msg

    jobApkFile = getJobApkFile()
    jobApkFileStr = os.path.abspath(jobApkFile)
    jobApkName = os.path.basename(jobApkFile)
    branch = os.environ["Branch"]

    copyApkName = jobApkName.replace(".apk", "(" + branch.replace("origin/", "") + ").apk")

    is_jiagu = os.environ["jiagu"] == "true"
    is_channel = os.environ["channel"] == "true"
    if is_jiagu and is_channel:
        downloadApkPath = os.path.dirname(jobApkFile)
    else:
        downloadApkPath = os.path.abspath(jobApkFile)

    jenkinsApkUrl = os.environ["JOB_URL"] + "/ws" + downloadApkPath.split(os.environ["WORKSPACE"])[1]
    print(jenkinsApkUrl)

    fileAndroidUrl = "http://10.10.10.78:8082/files/android/"
    fileAndroidPath = "/files/android/"
    qrcodePath = "qrcode/"
    apkPath = "apk/"
    copyApkFileStr = fileAndroidPath + apkPath + copyApkName
    shutil.copy(jobApkFileStr, copyApkFileStr)
    os.chmod(copyApkFileStr, 0777)
    deleteOldestFile(fileAndroidPath + apkPath, 50)

    apkUrl = fileAndroidUrl + apkPath + copyApkName
    print("apkUrl=" + apkUrl)
    qrcodeImgName = copyApkName + ".png"
    qrcodeImgFile = fileAndroidPath + qrcodePath + qrcodeImgName
    makeQRCodeImg(apkUrl, qrcodeImgFile)
    os.chmod(qrcodeImgFile, 0777)
    deleteOldestFile(fileAndroidPath + qrcodePath, 50)

    buildQRCodeURL = fileAndroidUrl + qrcodePath + qrcodeImgName
    print("qrcodeUrl=" + buildQRCodeURL)

    atPersonsString = os.getenv("at_persons", "").strip()  # 选择已经录入的人
    atMobileString = os.getenv("at_mobiles", "").strip()   # 指定手机号
    remark_msg = os.getenv("remark_msg", "").strip()
    print(atPersonsString)
    if len(atPersonsString) != 0 and atPersonsString[len(atPersonsString) - 1] != ",":
        concatChar = "," if atPersonsString[len(atPersonsString) - 1] != "," else ""
        atMobileString = atPersonsString + concatChar + atMobileString
    if len(atMobileString) == 0:
        atMobileList = []
    else:
        atMobileList = atMobileString.split(",")
    remarkString = ""
    for mobile in atMobileList:
        if len(mobile) != 11:
            continue
        remarkString = remarkString + ("@" + mobile + " ")
    remarkString = remarkString + remark_msg
    if len(remarkString) != 0:
        remarkString = " \n* " + remarkString
    # 配置发送dingtalk通知的请求参数
    body = {
            "actionCard": {
                "title": copyApkName,
                "text": "**" + copyApkName + "** \n* " +
                        msg + " \n* " +
                        commit + remarkString,
                "hideAvatar": "0",
                "btnOrientation": "1",
                "btns": [
                    {
                        "title": "点击下载",
                        "actionURL": apkUrl
                    },
                    {
                        "title": "jenkins apk",
                        "actionURL": jenkinsApkUrl
                    },
                    {
                        "title": "扫描二维码",
                        "actionURL": buildQRCodeURL
                    }
                ]
            },
            "at": {
                "atMobiles": atMobileList,
                "isAtAll": False
            },
            "msgtype": "actionCard"
    }

    dataJson = json.dumps(body)
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + os.environ["dingtalk_access_token"]
    send_cmd = "curl -H \'Content-Type: application/json\' -d \'" + dataJson + "\' " + url
    resp = os.popen(send_cmd).read()
    print(resp)


send_appQRCodeURL_to_dingtalk()
