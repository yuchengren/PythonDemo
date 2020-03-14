from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def select(driver: WebDriver, first_menu_index: int, second_menu_index: int, third_menu_index: int):
    # 点击CRM系统
    crmSystemElement = driver.find_element_by_class_name("menu___1QsMw").find_elements_by_class_name("menu-item___3QMia")[first_menu_index]
    crmSystemElement.click()
    # 点击个人工作台
    subMenu = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "sider___1t24v")))
    personalConsole = subMenu.find_elements_by_class_name("ant-menu-submenu")[second_menu_index]
    personalConsole.click()
    # 点击我的公海
    inlineMenu = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//ul[contains(@id,"$Menu")]')))
    myPublicSea = inlineMenu.find_elements_by_class_name("ant-menu-item")[third_menu_index]
    myPublicSea.click()

    iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))  # 我的公海iframe区域
    driver.switch_to.frame(iframe)
