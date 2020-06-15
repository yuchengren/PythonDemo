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

imgFilePath = os.environ['HOME'] + "/veryeast_img1/"

for i in os.listdir(imgFilePath):
    char = os.path.basename(i).split("_")[0]
    if len(char) != 4:
        print(char )


