import urllib
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import datetime
import pymysql
import os
import re
from sqlalchemy import create_engine
import datetime


#역으로 리스트 출력 
#input : 시작(큰 수), 끝(작은 수) 
def make_list_desc(start, end):
    temp = []
    for i in range(start, end-1, -1):
        temp.append(i)
    return temp




aladin_week_url = 'https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&Year={}&Month={}&Week={}&page={}}&cnt=1000&SortOrder=1'
aladin_month_url = 'https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=MonthlyBest&BranchType=1&CID=0&Year={}&Month={}&Week=3&page={}&cnt=1000&SortOrder=1'
#주간
#https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&Year=2020&Month=11&Week=3&page=4&cnt=1000&SortOrder=1
#https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&Year={}&Month={}&Week={}&page={}}&cnt=1000&SortOrder=1
#월간
#월간이면 Week 3으로 고정
#https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=MonthlyBest&BranchType=1&CID=0&Year=2016&Month=11&Week=3&page=5&cnt=1000&SortOrder=1
#https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=MonthlyBest&BranchType=1&CID=0&Year={}&Month={}&Week={}&page={}&cnt=1000&SortOrder=1
# 구분 : 주간이면 
# BestType= Bestseller 
# BestType= MonthlyBest

#https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0
def aladin_week(year, month, week, page):

    aladin_data =pd.DataFrame(columns=['date','rank','title','review','auther'])

    url = aladin_week_url.format(year, month, week, page)
    response = urllib.request.urlopen(url)
    soup = bs(response, 'html.parser')
    result = soup.select('div.ss_book_box')
    
#Myform > div:nth-child(3)
#Myform > div:nth-child(4)
#table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > div
    for i, post in enumerate(result):
        try:
            week_date = str(year)+ str(month) + str(week)
            #Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > div
            #table/tbody/tr/td[1]/table/tbody/tr[1]/td/div
            rank =  post.select_one('table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > div').text
            #Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(2) > a.bo3 > b
            title = post.select_one('a.bo3 > b').text
            #Myform > div:nth-child(6) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(4) > a
            review = post.select_one('table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(4) > a').text
            ##Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(1)
            auther = post.select_one('ul > li:nth-child(3) > a:nth-child(1)').text
            #Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(3)
            #publishor = post.select_one('table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(3)').text
            df = pd.DataFrame({'date' : week_date, 'rank':rank,'title': title,'review':review,'auther':auther}, index = [0])
            aladin_data = pd.concat([aladin_data, df])
        except AttributeError as e:
            print(e)
            print(i)
            pass

    aladin_data['date'] = week_date
    engine = create_engine("mysql+pymysql://root:0000@localhost/aladin", encoding= 'utf-8')
    conn = engine.connect()
    # con = pymysql.connect(host='localhost',
    #                         port=3306,
    #                         user='root',
    #                         password='0000',
    #                         db='aladin',
    #                         charset='utf8')
    #                         #database 이름 변경
    # #db = ''
    # engine = create_engine('mysql+pymysql://root:0000@localhost/aladin', 'utf8')
    aladin_data.to_sql('aladin_all_week',if_exists = 'append', con = engine)
    conn.close()

    # con.commit()   

def aladin_month(year, month, page):

    aladin_data =pd.DataFrame(columns=['date','rank','title','review','auther'])

    url = aladin_month_url.format(year, month, page)
    response = urllib.request.urlopen(url)
    soup = bs(response, 'html.parser')
    result = soup.select('div.ss_book_box')
#Myform > div:nth-child(3)
#Myform > div:nth-child(4)
#table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > div
    for i, post in enumerate(result):
        try:
            month_date = str(year)+ str(month) 

            #Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > div
            #table/tbody/tr/td[1]/table/tbody/tr[1]/td/div
            rank =  post.select_one('table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > div').text
            #Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(2) > a.bo3 > b
            title = post.select_one('a.bo3 > b').text
            #Myform > div:nth-child(6) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(4) > a
            review = post.select_one('table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(4) > a').text
            ##Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(1)
            auther = post.select_one('ul > li:nth-child(3) > a:nth-child(1)').text
            #Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(3)
            #publishor = post.select_one('table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(3)').text
            df = pd.DataFrame({'date': month_date, 'rank':rank,'title': title,'review':review,'auther':auther}, index = [0])
            aladin_data = pd.concat([aladin_data, df])
        except AttributeError as e:
            print(e)
            print(i)
            pass


    # con = pymysql.connect(host='localhost',
    #                         port=3306,
    #                         user='root',
    #                         password='0000',
    #                         db='aladin',
    #                         charset='utf8')
    #                         #database 이름 변경
    # #db = ''
    # engine = create_engine('mysql+pymysql://root:0000@localhost/aladin',encoding= 'utf8')
    engine = create_engine("mysql+pymysql://root:0000@localhost/aladin", encoding= 'utf-8')
    conn = engine.connect()
    aladin_data.to_sql('aladin_all_month',if_exists = 'append', con = engine)
    conn.close()
#    con.commit()   

if __name__ == "__main__":
    year_list = make_list_desc(2022,2000)

    month_list = make_list_desc(12,1)

    week_list = make_list_desc(5,1)

    for byear in year_list : 
        for bmonth in month_list:
            for i in range(1,6):
                aladin_month(byear, bmonth, i)
    for byear in year_list : 
        for bmonth in month_list:
            for bweek in week_list:
                for i in range(1,6):
                    aladin_week(byear, bmonth,bweek, i)





