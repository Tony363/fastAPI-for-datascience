import alpaca_trade_api as tradeapi
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, HTTPException, Query, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

api_key = api_key
api_secret = api_secret
base_url = base_url

app = FastAPI()

@app.post("/alpaca/{stock_id_list}/{timeframe}")
async def barrs(stock_id_list,timeframe,limit = 20):#token: str = Depends(oauth2_scheme)):
    api = tradeapi.REST(api_key,api_secret,base_url,api_version='v2')
    account = api.get_account()

    stock_id_list = stock_id_list.replace(">","").split("<")
    stock_id_list = [i.upper() for i in stock_id_list]

    if len(stock_id_list[1:]) > int(limit):
        return {"Query_Limit":"Exceeded Query Limit"}

    data = dict()
    for stock in stock_id_list[1:]:      
        try:
            bar = api.get_barset(stock,timeframe,limit=2)
            STD = (bar[stock][1].c - bar[stock][0].c)/ bar[stock][1].c
        except IndexError as e:
            return {"Query Error":"one of your queried stocks does not exist"}
        except Exception as e:
            return {"Timeframe Error":{"please choose":{'minute','1Min','5Min','15Min','day','1D'}}}
            
        data[stock] = dict()
        data[stock]["ID"] = stock
        data[stock]["SDT"] = STD
        data[stock]["Price_Now"] = bar[stock][-1].c

    return data