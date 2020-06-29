# coding: utf-8
import os
import sys

import configparser as configparser


def getConfigParser(_file):
    cp = configparser.ConfigParser()
    cp.read(_file)
    return cp


def getConfig(_file, section, option, fallback=""):
    cp = configparser.ConfigParser()
    cp.read(_file)
    return cp.get(section, option, fallback=fallback)

