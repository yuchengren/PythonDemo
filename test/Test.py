import datetime
import os
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from tensorflow.tools.compatibility import tf_upgrade_v2

from base.utils import TimeUtils

from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from veryeast.config import veryeast_config

imgFilePath = os.environ['HOME'] + "/veryeast_img1/"
time.time()
print((TimeUtils.parseToDatetime(str(datetime.date.today()) + " " + str(12) + ":00",
                                                TimeUtils.FORMAT_YEAR_MONTH_DAY_HOUR_MINUTE_HYPHEN) - datetime.datetime.now()).seconds)

