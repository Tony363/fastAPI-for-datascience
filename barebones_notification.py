import yfinance as yf
from datetime import datetime
from threading import Timer

x = datetime.today()
y = x.replace(day=x.day+1, hour=14, minute=40, second=0, microsecond=0)
delta_t = y-x

secs = delta_t.seconds+1

def hello_world():
    print("hello world")

t = Timer(secs, hello_world)
t.start()