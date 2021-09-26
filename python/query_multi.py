from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from driver import Driver
from bs4 import BeautifulSoup
import time
import pandas as pd
import tweet
import math
import filewriter as fw 
import threading
import os 
import sys
import numpy as np

os.chdir(r'C:\Users\Bloempot\Documents\Programming\trend_forecast_beta\python')
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

def create_query_string(accounts):
    query_string = ''
    for account in accounts:
        query_string = query_string + account + ', '
    return query_string

def calculate_query_string_size(amount_of_drivers, length):
    return math.ceil(length/amount_of_drivers)


''' MAIN PROGRAM'''
start_time = 0
amount_of_drivers = 1
n_watchdogs = 1
watchdog_accounts = ['elonmusk']
words_driver_1 = ['Bitcoin', 'BTC']

#start main drivers
drivers = []
    
for i in range(amount_of_drivers):
    drivers.append(Driver())

threads=[]

print("LOG: starting drivers "+Driver.debug_get_time())

for driver in drivers:
    threads.append(threading.Thread(target=Driver.start_chromedriver, args=[driver,]))
    threads[-1].start()
for thread in threads:
    thread.join()

print('LOG: Drivers started '+Driver.debug_get_time())
print('LOG: creating search queries'+Driver.debug_get_time())

while True:
    if time.time() - start_time > 180:
        start_time = time.time()
        Driver.set_search_query_strings_words(
            words_driver_1)

        print('LOG: Starting query'+Driver.debug_get_time())
        tweets = Driver.query_tweets_from_user(drivers)

        print('LOG: WRITING'+Driver.debug_get_time())

        filewriter = fw.FileWriter()
        filewriter.write_json('Data/Tweets.json', tweets)
        

    else: time.sleep(10)