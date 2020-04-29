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

from base.selenium import ElementUtils
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
follow_up_first_day_interval_today = 1  # 将要跟进客户的日期距离今天的天数
can_not_follow_up_days = ["2020-05-01", "2020-05-04", "2020-05-05", "2020-06-25", "2020-06-26",
                          "2020-10-01", "2020-10-02", "2020-10-05", "2020-10-06", "2020-10-07", "2020-10-08"]
weekend_is_weekdays = ["2020-04-26", "2020-05-09", "2020-06-28", "2020-09-27", "2020-10-10"]

# 浏览器
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path="chromedriver", options=options)
bg_system_login.login(driver)
select_three_menus.select(driver, first_menu_index, second_menu_index, third_menu_index)

today = datetime.datetime.now()
nextFollowUpstartDay = TimeUtils.formatToDayStr(today + datetime.timedelta(days=-conditionNextFollowUpIntervalDay))
nextFollowUpEndDay = TimeUtils.formatToDayStr(today + datetime.timedelta(days=follow_up_first_day_interval_today - 1))


def isDayCanFollowUp(day):
    _canAddFollowUpDayStr = TimeUtils.formatToDayStr(day)
    return TimeUtils.isWeekday(day) and _canAddFollowUpDayStr not in can_not_follow_up_days or \
           TimeUtils.isWeekend(day) and _canAddFollowUpDayStr in weekend_is_weekdays


canAddFollowUpDayList = []
canAddFollowUpDayDict = {}
canAddFollowUpDatetime = today + datetime.timedelta(days=follow_up_first_day_interval_today)
while len(canAddFollowUpDayList) < maxFollowUpForwardDays:
    if isDayCanFollowUp(canAddFollowUpDatetime):
        canAddFollowUpDayList.append(TimeUtils.formatToDayStr(canAddFollowUpDatetime))
    canAddFollowUpDatetime = canAddFollowUpDatetime + datetime.timedelta(days=1)
print(canAddFollowUpDayList)
currentAllocateDateStr = canAddFollowUpDayList[0]
print("currentAllocateDate = %s" % currentAllocateDateStr)
mainWindow = driver.current_window_handle


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
    time.sleep(0.2)  # 防止上次的事件选择框还未消失
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "ant-calendar-picker-container-placement-bottomLeft")))
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-calendar-input")))
    followUpInput = driver.find_element_by_class_name("ant-calendar-input")
    driver.execute_script("arguments[0].value='';", followUpInput)
    followUpInput.send_keys(end_time)
    driver.find_elements_by_class_name("_2-cVhQR")[0].click()  # 搜索
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))


def getListTotalNumber():
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
    time.sleep(0.2)
    totalElement = ElementUtils.findElement(driver, By.CLASS_NAME, "ant-pagination-total-text")
    if totalElement is None:
        return 0
    return int(totalElement.text.split("共")[1].split("条")[0].strip())


def getPageCount():
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
    totalElement = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-select-selection-selected-value")))
    return int(totalElement.text.split("条/页")[0].strip())


def changePageCountToMax():
    page_count_parent_el = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-pagination-options-size-changer")))
    page_count_el = page_count_parent_el.find_element_by_class_name("ant-select-selection")
    page_count_el.click()
    page_count_select_pop_id = page_count_el.get_attribute("aria-controls")
    page_count_select_pop = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, page_count_select_pop_id)))
    page_count_select_options = page_count_select_pop.find_element_by_tag_name("ul").find_elements_by_tag_name("li")
    page_count_select_options[-1].click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
    WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))


changePageCountToMax()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_1VePUHA")))  # 筛选条件区域
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-calendar-picker-icon")))
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-calendar-picker-input")))
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

nextPageElement = None
while nextPageElement is None or nextPageElement.get_attribute("aria-disabled") == "false":
    if nextPageElement is not None:
        driver.find_elements_by_class_name("_2-cVhQR")[0].click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
    WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
    listElement = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-tbody")))
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ant-table-row")))
    listRows = listElement.find_elements_by_class_name("ant-table-row")
    # 当前页客户的跟进
    for index, row in enumerate(listRows):
        row.find_elements_by_tag_name("td")[11].find_element_by_tag_name("a").click()  # 点击跟进客户
        all_windows = driver.window_handles
        driver.switch_to.window(all_windows[len(all_windows) - 1])
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "dRadioText-101")))
        # 是否纯粹安排 点击是
        driver.find_element_by_id("dRadioText-101").find_elements_by_class_name("ant-radio-input")[1].click()
        driver.find_element_by_class_name("ant-calendar-picker-input").click()
        nextFollowUpDatePop = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ant-calendar-picker-container-placement-bottomLeft")))
        fullFollowUpDayCount = 0
        for (k, v) in canAddFollowUpDayDict.items():
            if v < maxEachDayFollowUpNumber:
                if currentAllocateDateStr != k:
                    currentAllocateDateStr = k
                    print("currentAllocateDate = %s" % k)
                break
            else:
                fullFollowUpDayCount += 1
        while fullFollowUpDayCount == len(canAddFollowUpDayDict):
            canAddFollowUpDatetime = TimeUtils.addDays(canAddFollowUpDatetime, 1)
            if isDayCanFollowUp(canAddFollowUpDatetime):
                canAddFollowUpDayDict[currentAllocateDateStr] = 0
                currentAllocateDateStr = TimeUtils.formatToDayStr(canAddFollowUpDatetime)
                print("currentAllocateDate = %s" % currentAllocateDateStr)

        nextFollowUpDateElement = nextFollowUpDatePop.find_element_by_class_name("ant-calendar-input")
        driver.execute_script("arguments[0].value='';", nextFollowUpDateElement)
        nextFollowUpDateElement.send_keys(currentAllocateDateStr)
        nextFollowUpDateElement.send_keys(Keys.ENTER)

        driver.find_element_by_class_name("ant-btn-primary").click()
        canAddFollowUpDayDict[currentAllocateDateStr] = canAddFollowUpDayDict[currentAllocateDateStr] + 1
        driver.switch_to.window(mainWindow)
        # 我的公海iframe区域
        iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
    # 下一页
    nextPageElement = driver.find_element_by_class_name("ant-pagination-next")

driver.find_elements_by_class_name("_2-cVhQR")[0].click()
print("follow up over")
os._exit(1)
