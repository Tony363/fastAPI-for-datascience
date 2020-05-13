from bs4 import BeautifulSoup 
from selenium import webdriver
import requests ,re ,string
import pandas as pd
import chromedriver_binary

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')

url = 'https://finance.yahoo.com/quote/%5EDJI/'

driver.get(url)

html = driver.execute_script('return document.body.innerHTML')
# page = requests.get(url)

soup = BeautifulSoup(html,'lxml')
# print(soup)

DJI = soup.find_all('span',{'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})
print(type(float(list(DJI)[0].text)))
# print([entry.text for entry in DJI])
