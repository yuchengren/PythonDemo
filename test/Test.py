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

from veryeast.config import veryeast_config

files = os.listdir(veryeast_config.SCREEN_IMG_DIR)
for f in files:
    base_name = os.path.basename(f)
    captcha = base_name.split("_")[0]
    if len(captcha) != 4:
        print(base_name)


