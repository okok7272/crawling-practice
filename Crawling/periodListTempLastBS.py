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
import urllib.request
    
def ff():    
    url='https://product.kyobobook.co.kr/bestseller/total?period=002&utm_source=google&utm_medium=cpc&utm_campaign=googleSearch&gt_network=g&gt_keyword=%EC%9D%B8%ED%84%B0%EB%84%B7%EB%AC%B8%EA%B3%A0&gt_target_id=kwd-310087765320&gt_campaign_id=9979905549&gt_adgroup_id=98010719662&gclid=CjwKCAiAmuKbBhA2EiwAxQnt73XZA542QiaDnYLcSRoVJD8hf37JMgZpmvG2fMpi2NCL6vzeB8GwlhoCoLUQAvD_BwE'
    html =urllib.request.urlopen(url).read()
    soup = bs(html, 'html.parser')
    #value_list = soup.select('div#mainDiv > main > section.contents_wrap aside > div > section > div.tab_wrap type_line justify ui-tabs ui-corner-all ui-widget ui-widget-content > div > div#tabRoot > div.list_sort_wrap > div.right_area > div.form_sel type_sm > select#selListType > option')
    value_list =soup.select('div.right_area > div[1] > select#selListType > option')
    for i in value_list:
        vl = i.attrs
        print(vl["value"])

#/html/body/
#div[3]/main/section[2]/div/section/div[2]/div/div[2]/div[1]/div/div[1]/select/option[1]
#  div#mainDiv > main > section.contents_wrap aside > div > section > div.tab_wrap type_line justify ui-tabs ui-corner-all ui-widget ui-widget-content > 
#  div > div#tabRoot > div.list_sort_wrap > div.right_area > div.form_sel type_sm > select#selListType > option

ff()