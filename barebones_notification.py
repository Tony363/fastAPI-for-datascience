import yfinance as yf
import smtplib, ssl
from datetime import datetime
from threading import Timer

def hello_world():
    print("hello world")
    


x = datetime.today()
y = x.replace(day=x.day+1, hour=17, minute=27, second=0, microsecond=0)
delta_t = y-x

secs = delta_t.seconds+1

t = Timer(secs, hello_world)
t.start()