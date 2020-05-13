import os,smtplib,schedule,time,datetime, websocket,json
import yfinance as yf
import requests 
import chromedriver_binary
from bs4 import BeautifulSoup 
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Timer

def on_message(ws,message):
            # sender_address='pythonemails333@gmail.com',
            # sender_pass=input("please input password: \n"),
            # receiver_address="pysolver33@gmail.com",
            # ):
    print(message)
    # data = json.loads(message)
    # print(data)
    # # print(type(message),message['data'][0]['p'])

 
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = 'Pairs Trading Algo'
    

    # DJI = yf.Ticker('DJI')
    # DJI_latest = DJI.history(
    #     start=datetime.date.today() - datetime.timedelta(1),
    #     end=datetime.date.today(),
    # )
  
    # try:
    #     price = data['data'][0]['p']
    #     print(price)
    #     if price + 100 < DJI_latest.Close[-1]:
    #         main_content = f"Dow Jones Index dropped by more than 100 points today"
    #         print(main_content)
    #     else:
    #         main_content = "its fine today"
    #         print(main_content)
    # except IndexError as e:
    #     print("no data")
    #     main_content = "no data"


    # message.attach(MIMEText(mail_content,'plain'))

    # session = smtplib.SMTP('smtp.gmail.com',587)
    # session.starttls()
    # session.login(sender_address,sender_pass)

    # text = message.as_string()
    # session.sendmail(sender_address,receiver_address,text)
    # session.quit()  

    # done = 'mail sent'
    # print(done)

def on_error(ws,error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    # ws.send('{"type":"subscribe","symbol":"AMZN"}')
    # ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')
    # ws.send('{"type":"subscribe","symbol":"$DJI"}')
  

def pairs_trading_algo():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=bql9nt7rh5rfdbi8mhm0",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":

    x = datetime.datetime.today()
    try:
        y = x.replace(day=x.day+1, hour=17, minute=1, second=0, microsecond=0)
    except Exception as e:
        y = x.replace(day=x.day, hour=17,minute=1,second=0,microsecond=0)
    delta_t = y-x

    secs = delta_t.seconds+1

    t = Timer(secs, pairs_trading_algo)
    t.start()