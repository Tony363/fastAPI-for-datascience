import os
import smtplib 
import time
import datetime
import yfinance as yf
import requests 
import pkg_resources.py2_warn

from bs4 import BeautifulSoup 
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Timer


def main(
    sender_address='pythonemails333@gmail.com',
    receiver_address = 'pysolver33@gmail.com',
    sender_pass = 'thefool363',
    ):
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
    url = 'https://finance.yahoo.com/quote/%5EDJI/'
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(html,'lxml')

    # not always reliable
    DJI = list(soup.find_all('span',{'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}))
    DJI_fl = float(DJI[0].text.replace(',',''))
   
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Dow Jones Notification'

    DJI_prev = yf.Ticker('DJI')
    DJI_latest = DJI_prev.history(
        start=datetime.date.today() - datetime.timedelta(1),
        end=datetime.date.today() + datetime.timedelta(1),
    )
    

    if DJI_fl + 100 < DJI_latest.Close[-1]:
        mail_content = f'Dow Jones Index dropped by {DJI_latest.Close[-1] - DJI_fl}'
    else:
        mail_content = "Dow Jones Index didn't drop drastically"

    message.attach(MIMEText(mail_content,'plain'))

    session = smtplib.SMTP('smtp.gmail.com',587)
    session.starttls()
    session.login(sender_address,sender_pass)
    text = message.as_string()
    session.sendmail(sender_address,receiver_address,text)
    session.quit()  

    done = 'mail sent'
    print(done)




if __name__ == "__main__":
    x = datetime.datetime.today()

    y = x.replace(day=x.day+1, hour=3, minute=20, second=0, microsecond=0)
    
    delta_t = y-x

    secs = delta_t.seconds+1

    t = Timer(secs, main)
    t.start()

    

   

    