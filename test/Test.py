import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


from base.utils import TimeUtils

from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

print((TimeUtils.parseToDatetime("2020年3月23日 10:45", "%Y年%m月%d日 %H:%M") - datetime.now()).seconds)

driver = webdriver.Chrome()
driver.get(url="")  # 打开网址
driver.back()  # 后退至上一页面
driver.forward()  # 前进至下一页面
driver.close()  # 关闭当前标签页
driver.quit()  # 退出浏览器并关掉进程

driver.current_window_handle  # 浏览器当前窗口的句柄
driver.window_handles  # 浏览器打开的窗口的句柄集合
driver.switch_to.window(driver.window_handles[0])  # 根据窗口的句柄，切换至指定窗口
driver.switch_to.frame(iframe_element)  # 根据找到的iframe元素，切到至当前窗口里的iframe
driver.switch_to.default_content()  # 回到主窗体
driver.switch_to.parent_frame()  # 返回到上级iframe

driver.current_url  # 当前窗口的url
driver.title  # 当前窗口的标题
driver.get_cookies()  # 获取当前的cook
driver.get_cookie("token")  # 根据name获取相应的cookie value
driver.add_cookie(cookie_dict)  # 添加cookie
driver.delete_cookie("token")  # 根据name删除相应的cookie
driver.delete_all_cookies()  # 删除所有的cookie
driver.get_screenshot_as_file(file_name)  # 获取当前窗口全屏截图


driver.find_element_by_id("id")  # 元素的id 具有唯一性
driver.find_element_by_class_name("class")  # 元素的类名
driver.find_elements_by_name("class")  # 元素的名称
driver.find_element_by_tag_name("tag")  # 元素的标签名
driver.find_element_by_xpath("xpath")  # 元素的相对/绝对路径
driver.find_element_by_css_selector("css_selector")  # 元素的css选择器
driver.find_element_by_link_text("link_text")  # 对于有链接式的元素，用文本定位
driver.find_element_by_partial_link_text("partial_link_text")  # 对于有链接式的元素，用文本部分匹配定位

driver.find_elements_by_class_name("class")  # 当前窗口的类名是xxx的所有元素

driver.find_element(By.ID, "kw")
driver.find_element(By.NAME, "wd")
driver.find_element(By.CLASS_NAME, "s_ipt")
driver.find_element(By.TAG_NAME, "input")
driver.find_element(By.LINK_TEXT, u"新闻")
driver.find_element(By.PARTIAL_LINK_TEXT, u"新")
driver.find_element(By.XPATH, "//*[@class='bg s_btn']")

driver.find_element(By.CSS_SELECTOR, "span.bg s_btn_wr>input#su")

"document.getElementsByName('wd')[0].value='selenium';"
"document.getElementsByTagName('wd')[0].value='selenium';"
"document.querySelectorAll('.s_ipt')[0].value='selenium';"
"document.getElementById('su').click();"
"document.getElementsByClassName('s_btn')[0].click()"

element = driver.find_element(By.ID, "kw")

select_element = Select(element)
select_element.select_by_index(0)
select_element.select_by_value("option1")
select_element.select_by_visible_text("选项1")
select_element.deselect_by_index(0)
select_element.deselect_all()
select_element.options
select_element.all_selected_options
select_element.first_selected_option

ActionChains(driver).move_to_element(element).perform()  # 鼠标移动到指定元素
ActionChains(driver).move_to_element_with_offset(element, 5, 5).click().perform()  # 鼠标移动到指定元素后点击

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "class value")))
EC.visibility_of_element_located


driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("www.baidu.com")
driver.find_element_by_id("su")

time.sleep(0.5)

