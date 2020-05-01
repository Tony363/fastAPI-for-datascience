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
print(soup)
