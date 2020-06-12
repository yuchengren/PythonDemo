# -*- coding: UTF-8 -*-
"""
跟进客户
"""
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime

from base.config import account
from base.selenium import ElementUtils
from veryeast.enum import ConditionEnums
from veryeast.common import bg_system_login
from veryeast.common import select_three_menus

from base.utils import TimeUtils

# 通用配置项
first_menu_index = ConditionEnums.HomeFirstMenu.crm_system.value
second_menu_index = ConditionEnums.CRMSystemChildMenu.personal_console.value
third_menu_index = ConditionEnums.PersonalConsoleChildMenu.my_customer.value

sys_args = sys.argv
print("sys_args= %s" % sys_args)
if len(sys_args) > 1:
    username = sys_args[1]
else:
    username = account.veryeast_username
if len(sys_args) > 2:
    pwd = sys_args[2]
else:
    pwd = account.veryeast_pwd
# 将要跟进客户的日期距离今天的天数
if len(sys_args) > 3 and sys_args[3]:
    follow_up_first_day_interval_today = int(sys_args[3])
else:
    follow_up_first_day_interval_today = 1
# 自动查询将要跟进日期开始往后的日期 跟进客户数量，限制查询的天数，再往后的没有查询到日期，默认当做客户数量为0
if len(sys_args) > 4 and sys_args[4]:
    query_follow_up_count_days = int(sys_args[4])
else:
    query_follow_up_count_days = 5
# 每天可安排的客户最大数量
if len(sys_args) > 5 and sys_args[5]:
    max_each_day_follow_up_count = int(sys_args[5])
else:
    max_each_day_follow_up_count = 55

# 验证码最多执行识别的次数
if len(sys_args) > 6 and sys_args[6]:
    max_captcha_recognise_times = int(sys_args[6])
else:
    max_captcha_recognise_times = 10
# 是否用tensorflow做验证码识别
if len(sys_args) > 7 and sys_args[7]:
    is_tensorflow_recognise_captcha = sys_args[7] != "false"
else:
    is_tensorflow_recognise_captcha = True

if len(sys_args) > 8:
    tujian_username = sys_args[8]
else:
    tujian_username = None
if len(sys_args) > 9:
    tujian_pwd = sys_args[9]
else:
    tujian_pwd = None

can_not_follow_up_days = ["2020-05-01", "2020-05-04", "2020-05-05", "2020-06-25", "2020-06-26",
                          "2020-10-01", "2020-10-02", "2020-10-05", "2020-10-06", "2020-10-07", "2020-10-08"]
weekend_is_weekdays = ["2020-04-26", "2020-05-09", "2020-06-28", "2020-09-27", "2020-10-10"]

is_jenkins_execute = len(sys_args) > 1
# 浏览器
options = webdriver.FirefoxOptions()
if is_jenkins_execute:
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Firefox(options=options)
bg_system_login.login(driver, username, pwd, max_captcha_recognise_times, is_tensorflow_recognise_captcha, tujian_username, tujian_pwd)
select_three_menus.select(driver, first_menu_index, second_menu_index, third_menu_index)

today = datetime.datetime.now()
nextFollowUpEndDay = TimeUtils.formatToDayStr(today + datetime.timedelta(days=follow_up_first_day_interval_today - 1))


def isDayCanFollowUp(day):
    _canAddFollowUpDayStr = TimeUtils.formatToDayStr(day)
    return TimeUtils.isWeekday(day) and _canAddFollowUpDayStr not in can_not_follow_up_days or \
           TimeUtils.isWeekend(day) and _canAddFollowUpDayStr in weekend_is_weekdays


canAddFollowUpDayList = []
canAddFollowUpDayDict = {}
canAddFollowUpDatetime = today + datetime.timedelta(days=follow_up_first_day_interval_today)
while len(canAddFollowUpDayList) < query_follow_up_count_days:
    if isDayCanFollowUp(canAddFollowUpDatetime):
        canAddFollowUpDayList.append(TimeUtils.formatToDayStr(canAddFollowUpDatetime))
    canAddFollowUpDatetime = canAddFollowUpDatetime + datetime.timedelta(days=1)
currentAllocateDateStr = canAddFollowUpDayList[0]
mainWindow = driver.current_window_handle


def clearAndInputCalendar(index, time_str):
    driver.find_elements_by_class_name("ant-calendar-picker-input")[index].click()
    if index > 0:
        time.sleep(0.2)  # 防止上次的事件选择框还未消失
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "ant-calendar-picker-container-placement-bottomLeft")))
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-calendar-input")))
    followUpInput = driver.find_element_by_class_name("ant-calendar-input")
    followUpInput.clear()
    if time_str:
        followUpInput.send_keys(time_str)


def resetNextFollowUpTimesAndSearchAgain(start_time, end_time):
    clearAndInputCalendar(0, start_time)
    clearAndInputCalendar(1, end_time)
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


def follow_up_filtered_customer():
    nextPageElement = None
    while nextPageElement is None or nextPageElement.get_attribute("aria-disabled") == "false":
        if nextPageElement is not None:
            driver.find_elements_by_class_name("_2-cVhQR")[0].click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-spin-holder")))
        listElement = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-tbody")))
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
            lastAllocateDateStr = currentAllocateDateStr
            while canAddFollowUpDayDict.get(currentAllocateDateStr, 0) >= max_each_day_follow_up_count:
                canAddFollowUpDatetime = TimeUtils.addDays(TimeUtils.parseToDatetime(currentAllocateDateStr), 1)
                if isDayCanFollowUp(canAddFollowUpDatetime):
                    currentAllocateDateStr = TimeUtils.formatToDayStr(canAddFollowUpDatetime)
            if lastAllocateDateStr != currentAllocateDateStr or currentAllocateDateStr == canAddFollowUpDayList[0]:
                print("currentAllocateDate = %s" % currentAllocateDateStr)
            nextFollowUpDateElement = nextFollowUpDatePop.find_element_by_class_name("ant-calendar-input")
            driver.execute_script("arguments[0].value='';", nextFollowUpDateElement)
            nextFollowUpDateElement.send_keys(currentAllocateDateStr)
            nextFollowUpDateElement.send_keys(Keys.ENTER)

            driver.find_element_by_class_name("ant-btn-primary").click()
            canAddFollowUpDayDict[currentAllocateDateStr] = canAddFollowUpDayDict.get(currentAllocateDateStr, 0) + 1
            driver.switch_to.window(mainWindow)
            # 我的公海iframe区域
            iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
            driver.switch_to.frame(iframe)
        # 下一页
        nextPageElement = driver.find_element_by_class_name("ant-pagination-next")

    driver.find_elements_by_class_name("_2-cVhQR")[0].click()
    print("follow up over")
    if not is_jenkins_execute:
        os._exit(1)


def main():
    changePageCountToMax()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_1VePUHA")))  # 筛选条件区域
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-calendar-picker-icon")))
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-calendar-picker-input")))
    # 获取跟进日期在今天以前的数据量
    resetNextFollowUpTimesAndSearchAgain("", nextFollowUpEndDay)
    waitFollowUpTotalNumber = getListTotalNumber()
    print("waitFollowUpTotalNumber=%d" % waitFollowUpTotalNumber)
    if waitFollowUpTotalNumber == 0:
        if is_jenkins_execute:
            return
        else:
            os._exit(1)

    # 获取未来指定分配的日期的数据量
    for i in canAddFollowUpDayList:
        resetNextFollowUpTimesAndSearchAgain(i, i)
        canAddFollowUpDayDict[i] = getListTotalNumber()
    print(canAddFollowUpDayDict)
    #  获取跟进日期在今天以前的数据列表
    resetNextFollowUpTimesAndSearchAgain("", nextFollowUpEndDay)
    # os._exit(1)
    follow_up_filtered_customer()


main()

