import os,smtplib,schedule,time,datetime
import yfinance as yf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Timer
from secrets import *



def pairs_trading_algo():
    print('WTF')
    stock = 'DJI'
    sender_address = 'pythonemails333@gmail.com'
    sender_pass = input('please input password: ')

    receiver_address = 'pysolver33@gmail.com'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Pairs Trading Algo'

    DJI = yf.Ticker('DJI')
    DJI_latest = DJI.history(
        start=datetime.date.today() - datetime.timedelta(1),
        end=datetime.date.today(),
    )

    if DJI_latest.Close.diff()[-1] >= 100:
        mail_content = f'Dow Jones Index dropped by {DJI_latest.Close.diff()[-1]}'


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
    stock = 'DJI'
  
    x = datetime.datetime.today()
    y = x.replace(day=x.day+1, hour=17, minute=46, second=0, microsecond=0)
    delta_t = y-x

    secs = delta_t.seconds+1

    t = Timer(secs, pairs_trading_algo)
    t.start()