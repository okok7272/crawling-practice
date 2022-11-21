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



def fuckingcrwaling(errornum):
#engine = create_engine("mysql+mysqldb://root:"+"password"+"@localhost/db_name", encoding='utf-8')
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    #driver=webdriver.Chrome('./Chromedriver')
    url='https://product.kyobobook.co.kr/bestseller/total?period=002&utm_source=google&utm_medium=cpc&utm_campaign=googleSearch&gt_network=g&gt_keyword=%EC%9D%B8%ED%84%B0%EB%84%B7%EB%AC%B8%EA%B3%A0&gt_target_id=kwd-310087765320&gt_campaign_id=9979905549&gt_adgroup_id=98010719662&gclid=CjwKCAiAmuKbBhA2EiwAxQnt73XZA542QiaDnYLcSRoVJD8hf37JMgZpmvG2fMpi2NCL6vzeB8GwlhoCoLUQAvD_BwE'
    driver.get(url)
    driver.maximize_window()

    time.sleep(2)
    engine = create_engine("mysql+pymysql://root:0000@localhost/koyboweek", encoding= 'utf-8')
    conn = engine.connect()
    try :
        firstclick1 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.burst_banner_wrap > button")))
        firstclick1.click()
    except Exception as e:
        pass
    for i in range(errornum,54):
        time.sleep(2)
        #driver.find_element(By.CSS_SELECTOR, "#selListType-button").send_keys(Keys.ENTER)
        try :
            firstclick1 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selListType-button")))
            firstclick1.click()
            driver.implicitly_wait(100)
        except Exception as e:
            pass
        time.sleep(2)
        try :
            weekChange = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#selListType-menu > li:nth-child({i})")))
            weekChange.click()
            driver.implicitly_wait(100)
        except Exception as e:
            pass
        time.sleep(2)
        driver.implicitly_wait(100)
        df = pd.DataFrame(columns=['단위', '기간', '카테고리', '순위', '제목', '저자출판사', '연도', '평점', '리뷰개수'])
        #데이터가 주간인지 파악해서 라벨링
        unit_size = driver.find_element(By.CSS_SELECTOR, '#mainDiv > main > section.contents_wrap.aside > div > aside > div.aside_body > div > ul > li:nth-child(1) > ul > li.snb_item.active > a').text

        #데이터가 몇주인지 파악해서 라벨링
        period = driver.find_element(By.CSS_SELECTOR, '#baseDateText').text
        #데이터가 종합인지 아닌지 파악해서 라벨링
        category = driver.find_element(By.CSS_SELECTOR, '#classificationList > ul > li.tab_item.swiper-slide.ui-state-active.swiper-slide-active > button > span').text
        for k in range(10):
            item1s = driver.find_elements(By.CSS_SELECTOR,'#tabRoot > div.view_type_list.switch_prod_wrap > ol:nth-child(1)>li')
            driver.implicitly_wait(100)

            for item in item1s:
                #순위 구현
                #div.prod_area.horizontal > div.prod_info_box > div.prod_rank > div > span > span
                #div.prod_area.horizontal > div.prod_info_box > div.prod_rank > div > span
                driver.implicitly_wait(100)
                rank = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > div.prod_rank > div > span').text
                driver.implicitly_wait(100)
                title = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > a > span').text
                driver.implicitly_wait(100)

                author = item.find_element(By.CSS_SELECTOR,'div.prod_area.horizontal > div.prod_info_box > span').text
                driver.implicitly_wait(100)
                time.sleep(1)
                year = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > span > span').text
                driver.implicitly_wait(100)
                review_score = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > div.prod_bottom > div > span.review_klover_box > span.review_klover_text.font_size_xxs').text
                driver.implicitly_wait(100)
                #리뷰 개수
                #tabRoot > div.view_type_list.switch_prod_wrap > ol:nth-child(1) > li:nth-child(1) > div.prod_area.horizontal > div.prod_info_box > div.prod_bottom > div > span.review_klover_box > span.review_desc
                review_num = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > div.prod_bottom > div > span.review_klover_box > span.review_desc').text
                driver.implicitly_wait(100)
                new_row = {'단위' : unit_size, '기간' : period, '카테고리' : category, '순위' : rank, '제목' : title, '저자출판사' : author, '연도' : year, '평점' : review_score, '리뷰개수' : review_num}
                df = df.append(new_row, ignore_index = True)
                #df.loc(unit_size, period, category, rank, title, author, year, review_score, review_num, one_comment)
            item2s = driver.find_elements(By.CSS_SELECTOR,'#tabRoot > div.view_type_list.switch_prod_wrap > ol:nth-child(3)>li')
            driver.implicitly_wait(100)
            for item in item2s:
                driver.implicitly_wait(100)
                rank = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > div.prod_rank > div > span').text
                driver.implicitly_wait(100)
                title = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > a > span').text
                driver.implicitly_wait(100)

                author = item.find_element(By.CSS_SELECTOR,'div.prod_area.horizontal > div.prod_info_box > span').text
                driver.implicitly_wait(100)
                time.sleep(1)
                year = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > span > span').text
                driver.implicitly_wait(100)


                review_score = item.find_element(By.CSS_SELECTOR, 'div.prod_area.horizontal > div.prod_info_box > div.prod_bottom > div > span.review_klover_box > span.review_klover_text.font_size_xxs').text
                driver.implicitly_wait(100)

                #리뷰 개수
                #tabRoot > div.view_type_list.switch_prod_wrap > ol:nth-child(1) > li:nth-child(1) > div.prod_area.horizontal > div.prod_info_box > div.prod_bottom > div > span.review_klover_box > span.review_desc
                review_num = item.find_element(By.CSS_SELECTOR, ' div.prod_area.horizontal > div.prod_info_box > div.prod_bottom > div > span.review_klover_box > span.review_desc').text
                driver.implicitly_wait(100)

                new_row = {'단위' : unit_size, '기간' : period, '카테고리' : category, '순위' : rank, '제목' : title, '저자출판사' : author, '연도' : year, '평점' : review_score, '리뷰개수' : review_num}
                df = df.append(new_row, ignore_index = True)
            #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#tabRoot > div.list_result_wrap > div.pagination > button.btn_page.next'))).click()
            time.sleep(2)
            #driver.find_element(By.CSS_SELECTOR,"#tabRoot > div.list_result_wrap > div.pagination > button.btn_page.next").send_keys(Keys.ENTER)
            #driver.find_element(By.CSS_SELECTOR, "btn_page next").send_keys(Keys.ENTER)
            #넘김 기능 
            driver.implicitly_wait(100)

            try :
                firstclick1 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tabRoot > div.list_result_wrap > div.pagination > button.btn_page.next")))
                firstclick1.click()
                driver.implicitly_wait(100)

            except Exception as e:
                pass
            time.sleep(2)
        driver.implicitly_wait(100)
        
        df.to_sql(name='kyoboWeekAll', con= engine, if_exists= 'append', index=False)
        print(i)
    conn.close()
    driver.quit()

fuckingcrwaling(2)

