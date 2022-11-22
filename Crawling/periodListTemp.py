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

    for i in range(errornum,54):
        time.sleep(2)
        #driver.find_element(By.CSS_SELECTOR, "#selListType-button").send_keys(Keys.ENTER)
        #기간 변경하기위해 처음 클릭
        try :
            firstclick1 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selListType-button")))
            firstclick1.click()
            driver.implicitly_wait(100)
        except Exception as e:
            pass
        time.sleep(2)
        #해당 기간 선택
        try :
            weekChange = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#selListType-menu > li:nth-child({i})")))
            weekChange.click()
            driver.implicitly_wait(100)
        except Exception as e:
            pass
        time.sleep(2)
        driver.implicitly_wait(100)
        #데이터가 몇주인지 파악해서 라벨링
        period = driver.find_element(By.CSS_SELECTOR, '#baseDateText').text
        period_num =  re.sub(r'[^0-9]', '', period)
        time.sleep(1)
        temp.append(period_num)
        temp = duplicate_check(temp)
        time.sleep(1)
    df['ymw'] = temp
    df.to_sql(name='week_list', con= engine, if_exists= 'append', index=False)

    driver.quit()

week_list(1)
