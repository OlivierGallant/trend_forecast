import math
import threading
import time
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from manipulator import extract_information_div
from tweet import Tweet

import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

''' a driver object is able to interact with a twitter page '''
class Driver:
    '''class constants'''
    #div.css-1dbjc4n.r-18u37iz > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu
    
    CSS_ROOT = '.r-1ljd8xs > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > section:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)'
    CSS_ARTICLE = '.r-1ljd8xs > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > section:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div'
    CSS_NAME = 'div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div:nth-child(1) > div > span'
    CSS_NAME_ID = 'div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div:nth-child(2) > div > span'
    CSS_TEXT = 'div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div > span'
    CSS_COMMENTS = 'div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(1) > div > div > div:nth-child(2) > span > span > span'
    CSS_REPOSTS = 'div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > div > div > div:nth-child(2) > span > span > span'
    CSS_LIKES = 'div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(3) > div > div > div:nth-child(2) > span > span > span'         
    CSS_FIRST_DIV = '#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1gm7m50.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > div > section > div > div > div'
    CSS_CIRCLE = 'div > div > div > div > svg > circle'
    CSS_LAST_DIV = '#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1gm7m50.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > div > section > div > div > div'
    CSS_NO_RESULT = '#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1gm7m50.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > div > div.css-1dbjc4n.r-d9fdf6.r-6wcr4z'
                #div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu > div:nth-child(2) > div:nth-child(2) > div
    
    TIME_WINDOW = 86400
    soup_list = []
    watchdog_list = []
    query_strings = []

    def __init__(self):
        None
    
    def start_chromedriver(driver):
        print(os.getcwd())
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        #options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--log-level=0')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #options.add_argument('--blink-settings=imagesEnabled=false')
        driver.driver = webdriver.Chrome(options=options)
        driver.driver.set_window_size(1000, 1000)

        time.sleep(0.1)
        time.sleep(2)

    def reformat_date(date): 
        date = date.replace('-', ',')
        date = date.replace('T', ',')
        date = date.replace(':', ',')
        date = date.replace('.', ',')
        date = date.replace('Z', '')
        return date.split(',')

    def debug_get_time():
        return '['+(datetime.now()).strftime("%H:%M:%S")+']'

    def convert_str_to_number(x):
        total_stars = 0
        num_map = {'K':1000, 'M':1000000, 'B':1000000000}
        if x.isdigit():
            total_stars = int(x)
        else:
            if len(x) > 1:
                total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
        return int(total_stars)

    def set_search_query_strings_words(
            words,
            date_from_year = None,
            date_from_month = None,
            date_from_day = None,
            date_to_year = None,
            date_to_month = None,
            date_to_day = None):


            search_start = 'https://twitter.com/search?q=('
            like_filter = '%20min_faves%3A200'
            if date_from_year == None:
                date = ''
            else:
                date = '%20until%3A'+str(date_to_year)+'-'+str(date_to_month)+'-'+str(date_to_day)+'%20since%3A'+str(date_from_year)+'-'+str(date_from_month)+'-'+str(date_from_day)

            search_end ='%20-filter%3Areplies&src=typed_query&f=live'
            
            count = 1
            temp_string = ''
            for i, word in enumerate(words):
                temp_string = temp_string + '%3A'+str(word)
                count += 1
                if count == 20 or (i+1) == len(words):
                    temp_string = temp_string + ')'
                    Driver.query_strings.append(search_start+temp_string+like_filter+date+search_end)
                    count = 1
                    temp_string = ''
                else:
                    temp_string = temp_string + ' OR '
            return None 

    def set_search_query_strings_accounts(
        accounts,
        date_from_year = None,
        date_from_month = None,
        date_from_day = None,
        date_to_year = None,
        date_to_month = None,
        date_to_day = None):


        search_start = 'https://twitter.com/search?q=('
        like_filter = '%20min_faves%3A80'
        if date_from_year == None:
            date = ''
        else:
            date = '%20until%3A'+str(date_to_year)+'-'+str(date_to_month)+'-'+str(date_to_day)+'%20since%3A'+str(date_from_year)+'-'+str(date_from_month)+'-'+str(date_from_day)

        search_end ='%20-filter%3Areplies&src=typed_query&f=live'

        '''for the accounts: %3A+str(name)+%20OR%20from%3A'''
        count = 1

        temp_string = ''
        for i, account in enumerate(accounts):
            temp_string = temp_string + 'from%3A'+str(account)
            count += 1
            if count == 20 or (i+1) == len(accounts):
                temp_string = temp_string + ')'
                Driver.query_strings.append(search_start+temp_string+like_filter+date+search_end)
                count = 1
                temp_string = ''
            else:
                temp_string = temp_string + ' OR '
        return None 

    def load_page_and_return_source(driver, query_strings):
        for query_string in query_strings:
            driver.driver.get(query_string)
            WebDriverWait(driver.driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, driver.CSS_SELECTOR_PAGE_LOADED)))

            soup = BeautifulSoup(driver.driver.page_source, 'html.parser')
            for div in soup.find_all('div', class_=driver.ARTICLE_BOX):
                Driver.watchdog_list.append(div)
                print(extract_information_div(div))
        return

    def get_elements(driver):
        while Driver.query_strings:
            '''element containers'''
            soup_temp = []
            elements_temp = []

            '''element locations'''
            last_el_y_locations = []
            new_el_y_locations = []

            '''counters'''
            counter = 0
            empty_page_flag = False

            '''start time'''
            time_now = datetime.utcnow()

            ''' try to get a query string'''
            try:
                query_string = Driver.query_strings.pop(-1)
            except:
                break

            # load search page
            driver.driver.get(query_string)

            '''empty page/load fail detection mechanism, it is dirty, but it works in a rigorous fashion'''
            try:
                WebDriverWait(driver.driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, Driver.CSS_ROOT+' > '+Driver.CSS_TEXT)))
            except:
                try:
                    if driver.driver.find_element_by_css_selector(Driver.CSS_NO_RESULT):
                        print("LOG: Empty page, before loop")
                        raise StopIteration
                except: 
                    print("LOG: No results"+str(Driver.debug_get_time()))
                    break
                try:
                    WebDriverWait(driver.driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, Driver.CSS_ARTICLE)))
                except:
                    empty_page_flag = True
                    print('empty PAGE FLAG')
                    break
                

            # get elements from freshly scrolled page
            time_start = time.time() 
            while not elements_temp and empty_page_flag == False:
                if time.time() - time_start > 30: 
                    print('LOG: stuck in loop')
                    break
                try:
                    elements_temp = driver.driver.find_elements_by_css_selector(Driver.CSS_ARTICLE)
                    try:
                        if elements_temp[-1].find_element_by_css_selector(Driver.CSS_CIRCLE):
                            elements_temp = []
                            raise StopIteration
                    except:
                        time.sleep(0.08)
                        None
                except NoSuchElementException:
                    print('LOG: No such element exception')
                    None
                try:
                    for element in elements_temp:
                        new_el_y_locations.append(element.location['y'])
                        soup_temp.append(element.get_attribute('innerHTML'))
                except:
                    new_el_y_locations = []
                    elements_temp = []
                    soup_temp = []

            if empty_page_flag == False:
                y_pos_last_el = new_el_y_locations[-1]

                scroll_height = y_pos_last_el
                #first scroll
                driver.driver.execute_script("window.scrollBy(0, "+str(scroll_height)+")")

                for id, soup in enumerate(soup_temp):
                    if new_el_y_locations[id] < new_el_y_locations[-1]:
                        Driver.soup_list.append(BeautifulSoup(soup, 'html.parser'))

            while True:
                # clear the temp elements
                empty_page_flag = False
                new_el_y_locations = []
                elements_temp = []
                soup_temp = []
                
                
                # check for empty_page_flag
                if empty_page_flag == True:
                    print('LOG: Empty_page_flag')
                    break

                # check if page is loaded
                try:
                    WebDriverWait(driver.driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, Driver.CSS_ROOT+' > '+Driver.CSS_NAME)))
                except:
                    print('EMPTY PAGE FLAG')
                    empty_page_flag = True

                # get elements from freshly scrolled page
                time_start = time.time()
                while not elements_temp:
                    if time.time() - time_start > 30: 
                        print('LOG: stuck in loop')
                        break
                    try:
                        elements_temp = driver.driver.find_elements_by_css_selector(Driver.CSS_ARTICLE)
                        try:
                            if elements_temp[-1].find_element_by_css_selector('div > div > div > div > svg > circle'):  
                                elements_temp = []                  
                                raise StopIteration 
                        except:
                            time.sleep(0.08) # 80ms sleep
                            None
                            
                    except NoSuchElementException:
                        print("LOG: No such element exception")
                        elements_temp = []
                        None
                    try:
                        for element in elements_temp:
                            new_el_y_locations.append(element.location['y'])
                            soup_temp.append(element.get_attribute('innerHTML'))
                    except:
                        new_el_y_locations = []
                        elements_temp = []
                        soup_temp = []

                # check if new elements have been spotted
                if new_el_y_locations[-1] >= y_pos_last_el: 
                    # check date
                    time_list = Driver.reformat_date(BeautifulSoup(soup_temp[-2],'html.parser').find_all('time')[0]['datetime']) 
                    time_tweet = datetime(int(time_list[0]), int(time_list[1]), int(time_list[2]), int(time_list[3]), int(time_list[4]), int(time_list[5]))
                    if (time_now - time_tweet).total_seconds() > Driver.TIME_WINDOW:
                        '''add new elements and quit loop'''
                        for id, soup in enumerate(soup_temp):
                            if new_el_y_locations[id] >= y_pos_last_el:
                                soup = BeautifulSoup(soup, 'html.parser')
                                # check date
                                try:
                                    time_list = Driver.reformat_date(soup.find_all('time')[0]['datetime'])
                                    time_tweet = datetime(int(time_list[0]), int(time_list[1]), int(time_list[2]), int(time_list[3]), int(time_list[4]), int(time_list[5]))
                                    if (time_now - time_tweet).total_seconds() < Driver.TIME_WINDOW:
                                        Driver.soup_list.append(soup)
                                except: 
                                    None
                        break
                    # find the first new element compared to the previous loop
                    for id, soup in enumerate(soup_temp):
                        if new_el_y_locations[id] >= y_pos_last_el:
                            if new_el_y_locations[id] < new_el_y_locations[-1]:
                                Driver.soup_list.append(BeautifulSoup(soup, 'html.parser'))
                    # calculate scroll height
                    scroll_height = new_el_y_locations[-1] - y_pos_last_el
                    '''only set scroll height when it's > 0'''
                    # set new last element location
                    y_pos_last_el = new_el_y_locations[-1]
                else: 
                    break

                # perform a scroll
                driver.driver.execute_script("window.scrollBy(0, "+str(scroll_height)+")")  
                time.sleep(0.1) # 200 ms sleep
        return None
    
    def extract_element(element):
        '''this function will extract an element into all its relevant content'''
        content = ''
        try:
            for span in element.select(Driver.CSS_TEXT):
                content = content + span.get_text()
                print(content)
        except:
            print('LOG: content container not found')
            return None
        if content == '':
            return None

        try:
            username = element.select(Driver.CSS_NAME)[0].get_text()
            username_id = element.select(Driver.CSS_NAME_ID)[0].get_text()
        except:
            print('LOG: user container not found')
            return None
        

        time = element.find_all('time')[0]['datetime']

        try:
            comments = Driver.convert_str_to_number(element.select(Driver.CSS_COMMENTS)[0].get_text().replace(',','.'))
        except:
            print('LOG: comment container not found')
            comments = 0
        
        try:
            reposts = Driver.convert_str_to_number(element.select(Driver.CSS_REPOSTS)[0].get_text().replace(',','.'))
        except:
            reposts = 0
        try:
            likes = Driver.convert_str_to_number(element.select(Driver.CSS_LIKES)[0].get_text().replace(',','.'))
        except:
            likes = 0

        return [
            username,
            username_id,
            content,
            time,
            comments,
            reposts,
            likes
        ]
   
    def query_watchdog(
        drivers,
        accounts):

        accounts = Driver.drivers_divide_accounts(len(drivers), accounts)

        for driver, account in zip(drivers, accounts):
            driver.create_search_query_strings(account)
            print(driver.query_strings)


        threads = []
        for driver in drivers:
            threads.append(threading.Thread(target=Driver.start_chromedriver, args=[driver,]))
            threads[-1].start()

        for thread in threads:
            thread.join()  

        while True:
            start = time.time()
            threads=[]
            for driver in drivers:
                threads.append(threading.Thread(target=Driver.load_page_and_return_source, args=[driver, driver.query_strings]))
                threads[-1].start()
            
            for thread in threads:
                thread.join(300)
                if thread.is_alive():
                    e.set()

            print(time.time() - start)

    def query_tweets_from_user(
        drivers):

        '''Performing the search'''
        Driver.soup_list = []
        threads = []
        for driver in drivers:
            threads.append(threading.Thread(target=Driver.get_elements, args=[driver]))
            threads[-1].start()

        for thread in threads:
            thread.join()

        print(len(Driver.soup_list))
        # collect everything:
        print('LOG: COLLECTING'+Driver.debug_get_time())
        tweets = []
        extracts = []
        for soup in Driver.soup_list:
            extracts.append(Driver.extract_element(soup))

        for extract in extracts:
            if extract != None:
                try:
                    for id, tweet in enumerate(tweets):
                        if tweet.get_date() == extract[3]:
                            if tweet.get_user() == extract[0]:
                                if tweet.get_content() == extract[2]:
                                    tweets[id] = Tweet(
                                        extract[0],
                                        extract[1],
                                        extract[2],
                                        extract[3],
                                        extract[4],
                                        extract[5],
                                        extract[6])
                                    raise StopIteration
                    tweets.append(Tweet(
                            extract[0],
                            extract[1],
                            extract[2],
                            extract[3],
                            extract[4],
                            extract[5],
                            extract[6]))
                except StopIteration:
                    None

        for tweet in tweets:
            tweet.content = tweet.content.replace('#',' ').replace('.', ' ').replace('@', ' ').replace(',', ' ')  .replace('/n','. ')    
        '''
        for id, tweet in enumerate(tweets):
            print(str(id)+tweet.get_content())'''
        total_likes = 0
        for tweet in tweets:
            total_likes += int(tweet.get_likes())
        print(total_likes)
        print('LOG: QUERY FINISHED'+Driver.debug_get_time())
        print('N_TWEETS='+str(len(tweets)))
        
        return tweets
        #return tweets

        