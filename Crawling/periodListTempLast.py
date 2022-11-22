import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import create_engine
import pandas as pd
import re
from bs4 import BeautifulSoup
import urllib.request

def duplicate_check(x):
    du_temp = dict.fromkeys(x)
    resoration_list = list(du_temp)
    return resoration_list

def week_list(errornum):
#engine = create_engine("mysql+mysqldb://root:"+"password"+"@localhost/db_name", encoding='utf-8')
    temp = []
    df = pd.DataFrame(columns=['ymw'])
    engine = create_engine("mysql+pymysql://root:0000@localhost/unitsize", encoding= 'utf-8')
    conn = engine.connect()
    time.sleep(2)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    #driver=webdriver.Chrome('./Chromedriver')
    url='https://product.kyobobook.co.kr/bestseller/total?period=002&utm_source=google&utm_medium=cpc&utm_campaign=googleSearch&gt_network=g&gt_keyword=%EC%9D%B8%ED%84%B0%EB%84%B7%EB%AC%B8%EA%B3%A0&gt_target_id=kwd-310087765320&gt_campaign_id=9979905549&gt_adgroup_id=98010719662&gclid=CjwKCAiAmuKbBhA2EiwAxQnt73XZA542QiaDnYLcSRoVJD8hf37JMgZpmvG2fMpi2NCL6vzeB8GwlhoCoLUQAvD_BwE'
    driver.get(url)
    driver.maximize_window()

    #배너 끄기
    try :
        firstclick1 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.burst_banner_wrap > button")))
        firstclick1.click()
    except Exception as e:
        pass
    periods = driver.find_elements(By.CSS_SELECTOR, 'selListType > option')
    for period in periods :
        week_period = period.get_attribute('value')
        temp.append(week_period)

    #selListType > option:nth-child(1)
        #period_num =  re.sub(r'[^0-9]', '', period)
    time.sleep(1)
    df['ymw'] = temp
    print(temp)
    df.to_sql(name='week_list', con= engine, if_exists= 'append', index=False)
    conn.close()
    driver.quit()

week_list(1)
