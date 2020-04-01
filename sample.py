import random
import socket
import sys
import os
import time
import xgboost as xgb
import yfinance as yf
import pandas as pd
import numpy as np
import arcade
import os
import math
import time
import socket
import json

import sys
import struct

from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

from sklearn.model_selection import train_test_split


# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {loaded_data = json.loads(data)
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# class User(BaseModel):
#     username: str
#     email: str = None 
#     full_name: str = None 
#     disabled: bool = None 

# class UserInDB(User):
#     hashed_password: str


# def fake_hash_password(password: str):
#     return "fakehashed" + password

# def get_user(db,username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)

# def fake_decode_token(token):
#     # this doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db,token)
#     return user

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authenitcation credentials",
#             headers={"WWW-Authenticate":"Bearer"}
#         )
#     return user

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400,detail="Inactive user")
#     return current_user

# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token":user.username,"token_type":"bearer"}

# @app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user

##############################################

class payload(BaseModel):
    # number: int = None
    # label1: str = None
    # label2: str = None
    name: str
  

@app.post("/simple_data/")
async def print_data(item:payload):
    print(item)
    return item

@app.get("/")
async def root():
    used = []
    digit = random.choice(range(1000,100000))#sys.maxsize
    if digit not in used:
        used.append(digit)
        return {"message": digit}
    elif digit in used:
        return {"message":'this is a used digit'}

@app.post("/prediction/{stock_id}")
async def predict(stock_id):#,token: str = Depends(oauth2_scheme)):
    loaded_model = xgb.Booster()
    loaded_model.load_model('xgbregression.model')
    stock = yf.Ticker(str(stock_id))
    history = stock.history(period='max')
    stock_changes = history.pct_change()
    
    stock_changes.drop(stock_changes.index[0],inplace=True)
    stock_changes = pd.concat([stock_changes.Close.shift(-i) for i in range(100)],axis=1)
    stock_changes.drop(stock_changes.index[-100:],inplace=True)
    stock_changes.columns = [ f'Days_{i}'for i in range(len(stock_changes.columns))]

    X = stock_changes.loc[:,"Days_1":]
    y = stock_changes.loc[:,'Days_0']
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
    
    dtrain = xgb.DMatrix(X_train,label=y_train,nthread=-1)
    dtest = xgb.DMatrix(X_test,label=y_test,nthread=-1)
    prediction = loaded_model.predict(dtest)
    prediction = pd.DataFrame(prediction).to_dict()
    
    return {"prediction":prediction}

@app.post("/TONY's/stock/{stock_id}")
async def read_items(stock_id):#,token: str = Depends(oauth2_scheme)):
    stock = yf.Ticker(str(stock_id))
    stock_info = stock.info
    history = stock.history(period='max').to_dict()

    return {"stock":stock_info,
            "history":history}

