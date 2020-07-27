from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement


def findElement(_driver: webdriver, by, value):
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


def findElement(parent_el: webelement, by, value):
    try:
        return parent_el.find_element(by, value)
    except NoSuchElementException:
        return None
    pass