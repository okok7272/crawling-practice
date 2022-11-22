import requests
import pandas as pd


#https://product.kyobobook.co.kr/api/gw/pub/pdt/best-seller/total?page=1&per=200&period=002&bsslBksClstCode=A
period_num = '002'
# for i in range(2,54):
#     print(i)


response = requests.get(f'https://product.kyobobook.co.kr/api/gw/pub/pdt/best-seller/total?page=1&per=200&period={period_num}&bsslBksClstCode=A')
print(response)