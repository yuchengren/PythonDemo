# -*- coding: UTF-8 -*-
"""
跟进客户
"""
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime

from veryeast.enum import ConditionEnums
from veryeast.common import bg_system_login
from veryeast.common import select_three_menus

from base.utils import TimeUtils

# 通用配置项
first_menu_index = ConditionEnums.HomeFirstMenu.crm_system.value
second_menu_index = ConditionEnums.CRMSystemChildMenu.personal_console.value
third_menu_index = ConditionEnums.PersonalConsoleChildMenu.my_customer.value
maxEachDayFollowUpNumber = 55
conditionNextFollowUpIntervalDay = 14  # 下次跟进开始日期和结束日期的间隔天数
maxFollowUpForwardDays = 5  # 跟进客户日期推前的最大天数
# 浏览器
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
bg_system_login.login(driver)
select_three_menus.select(driver, first_menu_index, second_menu_index, third_menu_index)

today = datetime.datetime.now()
nextFollowUpstartDay = TimeUtils.formatToDayStr(today + datetime.timedelta(days=-conditionNextFollowUpIntervalDay))
nextFollowUpEndDay = TimeUtils.formatToDayStr(today)

canAddFollowUpDayList = []
canAddFollowUpDayDict = {}
canAddFollowUpDay = today + datetime.timedelta(days=1)
while len(canAddFollowUpDayList) < maxFollowUpForwardDays:
    if TimeUtils.isWeekday(canAddFollowUpDay):
        canAddFollowUpDayList.append(TimeUtils.formatToDayStr(canAddFollowUpDay))
    canAddFollowUpDay = canAddFollowUpDay + datetime.timedelta(days=1)
print(canAddFollowUpDayList)
currentAllocateDate = canAddFollowUpDayList[0]
print("currentAllocateDate = %s" % currentAllocateDate)
mainWindow = driver.current_window_handle
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_1VePUHA")))  # 筛选条件区域


def resetNextFollowUpTimesAndSearchAgain(start_time, end_time):
    if len(start_time) == 0:
        driver.find_elements_by_class_name("ant-calendar-picker-icon")[0].click()
    else:
        driver.find_elements_by_class_name("ant-calendar-picker-input")[0].click()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "ant-calendar-picker-container-placement-bottomLeft")))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-calendar-input")))
        followUpInput = driver.find_element_by_class_name("ant-calendar-input")
        driver.execute_script("arguments[0].value='';", followUpInput)
        followUpInput.send_keys(start_time)

    driver.find_elements_by_class_name("ant-calendar-picker-input")[1].click()
    time.sleep(0.2)   # 防止上次的事件选择框还未消失
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "ant-calendar-picker-container-placement-bottomLeft")))
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-calendar-input")))
    followUpInput = driver.find_element_by_class_name("ant-calendar-input")
    driver.execute_script("arguments[0].value='';", followUpInput)
    followUpInput.send_keys(end_time)
    searchBtn = driver.find_elements_by_class_name("_2-cVhQR")[0]
    searchBtn.click()
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))


def getListTotalNumber():
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
    totalElement = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-pagination-total-text")))
    return int(totalElement.text.split("共")[1].split("条")[0].strip())


def getPageCount():
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
    totalElement = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-select-selection-selected-value")))
    return int(totalElement.text.split("条/页")[0].strip())


# 获取跟进日期在今天以前的数据量
resetNextFollowUpTimesAndSearchAgain("", nextFollowUpEndDay)
waitFollowUpTotalNumber = getListTotalNumber()
print("waitFollowUpTotalNumber=%d" % waitFollowUpTotalNumber)

# 获取未来指定分配的日期的数据量
for i in canAddFollowUpDayList:
    resetNextFollowUpTimesAndSearchAgain(i, i)
    canAddFollowUpDayDict[i] = getListTotalNumber()
print(canAddFollowUpDayDict)

#  获取跟进日期在今天以前的数据列表
resetNextFollowUpTimesAndSearchAgain("", nextFollowUpEndDay)
listElement = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-tbody")))
listRows = listElement.find_elements_by_class_name("ant-table-row")
nextPageElement = None

while nextPageElement is None or nextPageElement.get_attribute("aria-disabled") == "false":
    if nextPageElement is not None:
        if nextPageElement.get_attribute("aria-disabled") == "false":
            nextPageElement.click()
        else:
            os._exit(1)
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
    time.sleep(0.5)
    listElement = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-tbody")))

    listRows = listElement.find_elements_by_class_name("ant-table-row")
    # 当前页客户的跟进
    for index, row in enumerate(listRows):
        row.find_elements_by_tag_name("td")[11].find_element_by_tag_name("a").click()  # 点击跟进客户
        all_windows = driver.window_handles
        driver.switch_to.window(all_windows[len(all_windows) - 1])
        # for window in all_windows:
        #     if window != mainWindow:
        #         driver.switch_to.window(window)
        #         break
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "dRadioText-101")))
        driver.find_element_by_id("dRadioText-101").find_elements_by_class_name("ant-radio-input")[
            1].click()  # 是否纯粹安排 点击是
        driver.find_element_by_class_name("ant-calendar-picker-input").click()
        nextFollowUpDatePop = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ant-calendar-picker-container-placement-bottomLeft")))
        fullFollowUpDayCount = 0
        for (k, v) in canAddFollowUpDayDict.items():
            if v < maxEachDayFollowUpNumber:
                if currentAllocateDate != k:
                    currentAllocateDate = k
                    print("currentAllocateDate = %s" % k)
                break
            else:
                fullFollowUpDayCount += 1
        if fullFollowUpDayCount == len(canAddFollowUpDayDict):
            lastFollowUpDayStr = canAddFollowUpDayDict.keys()[len(canAddFollowUpDayDict.keys()) - 1]
            lastFollowUpDay = TimeUtils.parseToDatetime(lastFollowUpDayStr)
            lastFollowUpDayWeekDay = lastFollowUpDay.weekday()
            needForwardDays = 1
            if lastFollowUpDayWeekDay == 4:
                needForwardDays = 3
            elif lastFollowUpDayWeekDay == 5:
                needForwardDays = 2
            currentAllocateDate = TimeUtils.formatToDayStr(TimeUtils.addDays(lastFollowUpDay, needForwardDays))
            print("currentAllocateDate = %s" % currentAllocateDate)
            canAddFollowUpDayDict[currentAllocateDate] = 0

        nextFollowUpDateElement = nextFollowUpDatePop.find_element_by_class_name("ant-calendar-input")
        driver.execute_script("arguments[0].value='';", nextFollowUpDateElement)
        nextFollowUpDateElement.send_keys(currentAllocateDate)
        nextFollowUpDateElement.send_keys(Keys.ENTER)

        driver.find_element_by_class_name("ant-btn-primary").click()
        time.sleep(0.2)
        # driver.close()
        canAddFollowUpDayDict[currentAllocateDate] = canAddFollowUpDayDict[currentAllocateDate] + 1
        driver.switch_to.window(mainWindow)
        iframe = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "iframe")))  # 我的公海iframe区域
        driver.switch_to.frame(iframe)

    # 点击下一页
    nextPageElement = driver.find_element_by_class_name("ant-pagination-next")




