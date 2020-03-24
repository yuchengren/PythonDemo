from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def findElement(_driver, by, value):
    try:
        return _driver.find_element(by, value)
    except NoSuchElementException:
        return None
    pass


def isElementExist(_driver, by, value):
    return findElement(_driver, by, value) is not None


def findElements(_driver, by, value):
    try:
        return _driver.find_elements(by, value)
    except NoSuchElementException:
        return None
    pass