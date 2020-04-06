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
import jwt
from jwt import PyJWTError

from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, HTTPException, Query, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext

from sklearn.model_selection import train_test_split

from secrets import *

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

SECRET_KEY = Key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
class User(BaseModel):
    username: str
    email: str = None 
    full_name: str = None 
    disabled: bool = None 

class UserInDB(User):
    hashed_password: str

class TokenData(BaseModel):
    username: str = None

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db,username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db,username:str,password:str):
    user = get_user(fake_db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

# def create_access_token(*,data:dict,expires_delta:timedelta=None):
#     to_encode = data.copy()
#     if expires_delta:
#         expires = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({'exp':expire})
#     encoded_jwt = jwt.encode((to_encode, SECRET_KEY,algorithm=ALGORITHM))
#     return encoded_jwt

def fake_decode_token(token):
    # this doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db,token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authenitcation credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token":user.username,"token_type":"bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

##############################################

data_frame = {'number':[],'label1':[],'label2':[]}

class payload(BaseModel):
    number: list = None
    label1: list = None
    label2: list = None
    
  

@app.post("/data/")
async def read_data(data: payload, request:Request):
    client_host = request.client.host
    data = dict(data)

    if data['number'][-1] in data_frame['number']:
        print('data already processed')
        print(data_frame)
        raise HTTPException(status_code=404,detail='data already processed')
    else:
        data_frame['number'].append(data['number'][-1])
        data_frame['label1'].append(data['label1'][-1])
        data_frame['label2'].append(data['label2'][-1])
        print(data_frame)

    return {'client_host':client_host,"data":data}

@app.post("/feed_data/")
async def feed_data(request:Request):  
    return data_frame

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
async def predict(stock_id,token: str = Depends(oauth2_scheme)):
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
async def read_items(stock_id,token: str = Depends(oauth2_scheme)):
    stock = yf.Ticker(str(stock_id))
    stock_info = stock.info
    history = stock.history(period='max').to_dict()

    return {"stock":stock_info,
            "history":history}

