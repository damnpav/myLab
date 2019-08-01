# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 03:40:24 2019

@author: hcani
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://finance.yahoo.com")
driver.close()