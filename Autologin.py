from breeze_connect import BreezeConnect
from tabulate import tabulate
from selenium import webdriver
from pyotp import TOTP
import urllib
import pandas as pd
import login as l
import numpy as np
from datetime import datetime
from time import time, sleep
import sys
import threading
import warnings
import time
import os

def autologin():
    browser=webdriver.Chrome()
    browser.get("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(l.api_key))
    browser.implicitly_wait(5)
    breeze = BreezeConnect(api_key=l.api_key)
    username = browser.find_element("xpath", '/html/body/form/div[2]/div/div/div[1]/div[2]/div/div[1]/input')
    password = browser.find_element("xpath", '/html/body/form/div[2]/div/div/div[1]/div[2]/div/div[3]/div/input')

    username.send_keys(l.userID)
    username.send_keys(l.password)

    #Checkbox
    browser.find_element("xpath", '/html/body/form/div[2]/div/div/div[1]/div[2]/div/div[4]/div/input').click()

    #Click login button
    browser.find_element("xpath", '/html/body/form/div[2]/div/div/div[1]/div[2]/div/div[5]/input[1]').click()
    time.sleep(2)
    pin = browser.find_element("xpath", '/html/body/form/div[2]/div/div/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/input').click()
    topt = TOTP(l.topt)
    token = topt.now()
    pin.send_keys(token)
    browser.find_element("xpath", '/html/body/form/div[2]/div/div/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/input').click()
    time.sleep(1)
    temp_token=browser.current_url.split('apisession=')[1][:8]
    #Save in database or text file
    print('temp_token is: ' , temp_token)
    breeze.generate_session(api_secret=l.api_secret, session_token=l.session_key)
    print(breeze.get_funds())
    browser.quit()

autologin()
