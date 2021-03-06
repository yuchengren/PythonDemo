# -*- coding: UTF-8 -*-
"""
揽入客户
"""
import os
import sys
import threading
import traceback

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from base.selenium import CookieUtils
from veryeast.enum import ConditionEnums
from veryeast.common import bg_system_login
from veryeast.common import select_three_menus

# 通用配置项
first_menu_index = ConditionEnums.HomeFirstMenu.crm_system.value
second_menu_index = ConditionEnums.CRMSystemChildMenu.personal_console.value
third_menu_index = ConditionEnums.PersonalConsoleChildMenu.my_public_sea.value
# 私有配置项
public_sea_condition_index = ConditionEnums.PublicSeaEnum.ve_marketing_center.value  # 筛选条件-所属公海
customer_source_index = ConditionEnums.CustomerSource.very_east_register.value  # 筛选条件-客户来源
except_customer_name = []  # 需要排除的客户名称
customer_name = ""
today = time.strftime("%Y-%m-%d")
startDay = today
endDDay = today

def select_filter_condition(driver):
    # 所属公海筛选-VE营销中心公海
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_1VePUHA")))  # 筛选条件区域
    # loading蒙层不可见后,待数据列表区域可见
    WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "ant-spin-blur")))
    print("cookies = %s" % CookieUtils.getCookiesStr(driver))
    belongPublicSeaElement = driver.find_element_by_xpath(
        '//*[@id="root"]/div/section/section/section/main/div/div/div/div/div[1]/div[2]/div[3]/div[2]/div/div')
    belongPublicSeaElement.click()
    publicSeaSelectPopId = belongPublicSeaElement.get_attribute("aria-controls")
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, publicSeaSelectPopId)))
    publicSeaSelectPop = driver.find_element_by_id(publicSeaSelectPopId)
    publicSeaSelectPop.find_elements_by_class_name("ant-select-dropdown-menu-item")[public_sea_condition_index].click()

    if customer_name:
        driver.find_elements_by_class_name("_7rOOrwL")[0].find_element_by_tag_name("input").send_keys(customer_name)
        return

    # 分配公海时间
    driver.find_element_by_class_name("ant-calendar-picker-Large").click()  # 开始日期~结束日期整体输入框
    dataPop = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-calendar-date-panel")))
    dataPopTimeInputs = dataPop.find_elements_by_class_name("ant-calendar-input")
    dataPopTimeInputs[0].send_keys(startDay)
    dataPopTimeInputs[1].send_keys(endDDay)

    # 展开更多条件-选择客户来源
    driver.find_elements_by_class_name("_2-cVhQR")[1].click()  # 点击展开更多条件

    more_condition_groups = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, '_29skZdk')))
    customerFrom = more_condition_groups[4].find_element_by_class_name("_3uDQ_Bd").find_element_by_class_name(
        "ant-select-selection")
    customerFrom.click()
    customerFromPopId = customerFrom.get_attribute("aria-controls")
    customerFromPop = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, customerFromPopId)))
    customerFromPop.find_elements_by_class_name("ant-select-dropdown-menu-item")[customer_source_index].click()
    # driver.find_elements_by_class_name("_1t34nAx")[1].click()  # 收起更多条件 后，更多条件的设置 搜索时不起作用


def get_in_customer(customer_index):
    # 浏览器
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    bg_system_login.login(driver)
    select_three_menus.select(driver, first_menu_index, second_menu_index, third_menu_index)
    select_filter_condition(driver)

    # 点击搜索
    driver.find_elements_by_class_name("_2-cVhQR")[0].click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-spin-blur")))  # loading蒙层可见后
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "ant-spin-blur")))  # loading蒙层不可见后
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ant-table-row")))
    tableRows = driver.find_elements_by_class_name("ant-table-row")
    if len(tableRows) <= customer_index:
        return
    tableRow = tableRows[customer_index]
    name_el = tableRow.find_element_by_tag_name("a")
    if name_el.text in except_customer_name:
        return
    name_el.click()
    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[len(all_windows) - 1])
    get_in_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/section/section/section/main/div/div/div/div/div/div[1]/div[2]/button[3]')))
    get_in_btn.click()
    WebDriverWait(driver, 10, 0.02).until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-btn-primary")))
    while True:
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(0.005)

customer_size = 1  # 可揽入客户的数量
thread_list = []
for index in range(customer_size):
    try:
        thread = threading.Thread(target=get_in_customer, args=(index, ))
        thread.start()
        thread_list.append(thread)
    except Exception as e:
        print("get in customer %s, occur exception:" % index)
        traceback.print_exc()

for t in thread_list:
    t.join()  # 线程A中使用B.join()表示线程A在调用join()处被阻塞，且要等待线程B的完成才能继续执行

os._exit(1)  # 防止程序执行完后，浏览器被自动关闭





