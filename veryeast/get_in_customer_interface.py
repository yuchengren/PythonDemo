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

from base.utils import UrlUtils
from veryeast.enum import ConditionEnums
from veryeast.common import bg_system_login
from veryeast.common import select_three_menus

# 通用配置项
first_menu_index = ConditionEnums.HomeFirstMenu.crm_system.value
second_menu_index = ConditionEnums.CRMSystemChildMenu.personal_console.value
third_menu_index = ConditionEnums.PersonalConsoleChildMenu.my_public_sea.value
# 私有配置项
public_sea_condition_index = ConditionEnums.PublicSeaEnum.recruit_fourth_part_prepare.value  # 筛选条件-所属公海
customer_source_index = ConditionEnums.CustomerSource.very_east_register.value  # 筛选条件-客户来源
except_customer_name = []  # 需要排除的客户名称
today = time.strftime("%Y-%m-%d")
startDay = today
endDDay = today

customer_dict_list = []

# 浏览器
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
bg_system_login.login(driver)
select_three_menus.select(driver, first_menu_index, second_menu_index, third_menu_index)
# 所属公海筛选-VE营销中心公海
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_1VePUHA")))  # 筛选条件区域
# loading蒙层不可见后,待数据列表区域可见
WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "ant-spin-blur")))

belongPublicSeaElement = driver.find_element_by_xpath(
    '//*[@id="root"]/div/section/section/section/main/div/div/div/div/div[1]/div[2]/div[3]/div[2]/div/div')
belongPublicSeaElement.click()
publicSeaSelectPopId = belongPublicSeaElement.get_attribute("aria-controls")
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, publicSeaSelectPopId)))
publicSeaSelectPop = driver.find_element_by_id(publicSeaSelectPopId)
publicSeaSelectPop.find_elements_by_class_name("ant-select-dropdown-menu-item")[public_sea_condition_index].click()

# 分配公海时间
driver.find_element_by_class_name("ant-calendar-picker-Large").click()  # 开始日期~结束日期整体输入框
dataPop = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "ant-calendar-date-panel")))
dataPopTimeInputs = dataPop.find_elements_by_class_name("ant-calendar-input")
# dataPopTimeInputs[0].send_keys(startDay)
# dataPopTimeInputs[1].send_keys(endDDay)

# 展开更多条件-选择客户来源
driver.find_elements_by_class_name("_2-cVhQR")[1].click()  # 点击展开更多条件
customerFrom = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH,'//*[@id="heiSearch"]/div/div[1]/div[2]/div[6]/div/div/div/div/div/div[2]/div/div')))
customerFrom.click()
customerFromPopId = customerFrom.get_attribute("aria-controls")
customerFromPop = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, customerFromPopId)))
customerFromPop.find_elements_by_class_name("ant-select-dropdown-menu-item")[customer_source_index].click()
# driver.find_elements_by_class_name("_1t34nAx")[1].click()  # 收起更多条件 后，更多条件的设置 搜索时不起作用

# 点击搜索
driver.find_elements_by_class_name("_2-cVhQR")[0].click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-spin-blur")))  # loading蒙层可见后
WebDriverWait(driver, 10).until_not(
    EC.visibility_of_element_located((By.CLASS_NAME, "ant-spin-blur")))  # loading蒙层不可见后
tableRows = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ant-table-row")))


def get_customers_info(index):
    _tableRows = driver.find_elements_by_class_name("ant-table-row")
    name_el = tableRows[index].find_element_by_tag_name("a")
    if name_el.text in except_customer_name:
        return
    name_el.click()
    current_handle = driver.current_window_handle
    for handle in driver.window_handles:
        if current_handle != handle:
            driver.switch_to.window(handle)
            customer_dict_list.append(UrlUtils.parseUrlParam(driver.current_url))
            driver.close()
            driver.switch_to.window(current_handle)
            iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))  # 我的公海iframe区域
            driver.switch_to.frame(iframe)
            break


for index in range(len(tableRows)):
    get_customers_info(index)



os._exit(1)









