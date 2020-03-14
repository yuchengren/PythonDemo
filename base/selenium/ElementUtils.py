from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def findElement(driver, by, value):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None
    pass


def findElements(driver, by, value):
    try:
        return driver.find_elements(by, value)
    except NoSuchElementException:
        return None
    pass