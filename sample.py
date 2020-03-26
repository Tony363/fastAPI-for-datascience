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

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

from sklearn.model_selection import train_test_split


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

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class User(BaseModel):
    username: str
    email: str = None 
    full_name: str = None 
    disabled: bool = None 

class UserInDB(User):
    hashed_password: str


def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db,username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

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
async def predict(stock_id):
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

@app.get("/TONY's/stock/{stock_id}")
async def read_items(stock_id,token: str = Depends(oauth2_scheme)):
    stock = yf.Ticker(str(stock_id))
    stock_info = stock.info
    history = stock.history(period='max').to_dict()

    return {"stock":stock_info,
            "history":history}


@app.get("/socket/server")
async def server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 12000))
    print('waiting for udp client')
     
    try:
        while True:
            server_socket.settimeout(10)  
            message, address = server_socket.recvfrom(1024)
            print('client received: {}'.format(address))
            print(message)
            send_message = bytes('connection established: index {}'.format(index), encoding='utf-8')
            server_socket.sendto(send_message, address)

    except socket.timeout:
        print('exceeded time')
        server_socket.close()

    except KeyboardInterrupt:
        print('time to close udp server')
        server_socket.shutdown(socket.SOCK_DGRAM)
    #     sys.exit(1)
    return {'server':'connected'}


@app.get("/socket/game_client/")
async def main():
    """ Main method """    
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
    table = window.get_table()
  
    return window.get_table()



"""
My Game Portion
"""
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

RECT_WIDTH = 700
RECT_HEIGHT = 500

SCREEN_TITLE = "Raymonds little games"

SHIP_SPEED = 5


class Shape:

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle
        self.color = color

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y
        self.angle += self.delta_angle

class Rectangle(Shape):

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
                                     self.color, self.angle)

class Triangle:
    def __init__(self,val_x,val_y,color):
        self.center_x = val_x
        self.center_y = val_y
        self.color = color
        self.x = self.center_x + 40 
        self.y = self.center_y
        self.x1 = self.center_x
        self.y1 = self.center_y - 100
        self.x2 = self.center_x + 80
        self.y2 = self.center_y -100
    
    def draw(self):
        arcade.draw_triangle_filled(self.center_x + 40, self.center_y,
                                    self.center_x, self.center_y - 100,
                                    self.center_x + 80, self.center_y -100,
                                    arcade.color.WHITE)

    # def draw(self):
    #     arcade.draw_triangle_filled(self.x, self.y,
    #                                 self.x1, self.y1,
    #                                 self.x2, self.y2,
    #                                 arcade.color.WHITE)

    #If f is your angle, (x,y) becomes (xcosf−ysinf,ycosf+xsinf).



    def triangle_follow(self,val_x,val_y):

        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        try:
            dest_x = val_x
            dest_y = val_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * SHIP_SPEED
            self.change_y = math.sin(angle) * SHIP_SPEED

            self.center_x += self.change_x
            self.center_y += self.change_y

            angle = 360-math.atan2(dest_x-300,dest_y-400)*180/math.pi

            self.angle = angle
        except Exception as e:
            print('error')
            pass
    
    def rotate(self):
        self.x = (math.cos(self.angle) * (self.center_x + 40)) - (math.sin(self.angle) * self.center_y)
        self.y = (math.cos(self.angle) * self.center_y) + (math.sin(self.angle) * (self.center_x + 40))

        self.x1 = (math.cos(self.angle) * self.center_x) - (math.sin(self.angle) * (self.center_y-100))
        self.y1 = (math.cos(self.angle) * self.center_y-100) + (math.sin(self.angle) * self.center_x )

        self.x2 = (math.cos(self.angle) * (self.center_x + 80)) - (math.sin(self.angle) * (self.center_y -100))
        self.y2 = (math.cos(self.angle) * self.center_y-100) + (math.sin(self.angle) * (self.center_x + 80))


       



          
          
       
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        self.shape_list = None
        self.triangle_list = None

        self.triangle_table = {}
        self.val_x = 700
        self.val_y = 500
    

        self.triangle = Triangle(self.val_x,self.val_y,arcade.color.WHITE)

        self.count = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.shape_list = []
        self.triangle_list = []

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawingtracking_table
        arcade.start_render()

        self.triangle.draw()
        
        for shape in self.shape_list:
            shape.draw()
        
        # for triangle in self.triangle_list:
        #     triangle.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)

        x = random.randrange(0, SCREEN_WIDTH)
        y = random.randrange(0, SCREEN_HEIGHT)
        width = random.randrange(10, 30)
        height = random.randrange(10, 30)
        angle = random.randrange(0, 360)

        d_x = random.randrange(-3, 4)
        d_y = random.randrange(-3, 4)
        d_angle = random.randrange(-3, 4)

        red = random.randrange(256)
        green = random.randrange(256)
        blue = random.randrange(256)
        alpha = random.randrange(256)

        shape_type = random.randrange(2)

        self.triangle.triangle_follow(self.val_x,self.val_y)

        
        hit_list = [(shape.x,shape.y) for shape in self.shape_list]

        for hit in self.shape_list: 

            if (int(self.triangle.center_x) in range(hit.x-50,hit.x+50)) and (int(self.triangle.center_y) in range(hit.y-50,hit.y+50)):
                self.shape_list.remove(hit)


        if  self.triangle.center_x < 50:
            self.triangle.center_x += 50

        elif self.triangle.center_x > SCREEN_WIDTH-50:
            self.triangle.center_x -= 50
        
        if self.triangle.center_y > SCREEN_HEIGHT-50:
            self.triangle.center_y -= 50
        
        elif self.triangle.center_y < 50:
            self.triangle.center_y += 50

        if len(self.shape_list) < 50:

            if (self.triangle.center_x < SCREEN_WIDTH//10 and self.triangle.center_x > 0) or (self.triangle.center_x > SCREEN_WIDTH - SCREEN_WIDTH//10  and self.triangle.center_x < SCREEN_WIDTH):

                shape = Rectangle(x, y, width, height, angle, d_x, d_y,
                                    d_angle, (red, green, blue, alpha))
                self.shape_list.append(shape)

            if (self.triangle.center_y < SCREEN_HEIGHT//10 and self.triangle.center_y > 0) or (self.triangle.center_y > SCREEN_HEIGHT - SCREEN_HEIGHT//10 and self.triangle.center_y < SCREEN_HEIGHT):

                shape = Rectangle(x, y, width, height, angle, d_x, d_y,
                                    d_angle, (red, green, blue, alpha))
                self.shape_list.append(shape)

        self.socket_connection()
         

    def on_mouse_press(self,x,y,button,modifiers):

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.count += 1
            self.val_x = x
            self.val_y = y
            self.triangle.rotate()
            # print(self.val_x,self.val_y)
       

            for count in range(self.count):
                if f'coor {self.count}' not in self.triangle_table: 
                    self.triangle_table[f'coor {self.count}'] = self.val_x,self.val_y
                elif f'coor {self.count}' in self.triangle_table:
                    continue
        
            
    
    def get_table(self):
        return self.triangle_table

    def socket_connection(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(5.0)
        message = b'connected'
        addr = ("127.0.0.1", 12000)
        start = time.time()
        client_socket.sendto(message,addr)

            
        try:
            data,server = client_socket.recvfrom(1024)
            end = time.time()
            elapsed = end - start
            print(f'{server} {data} {elapsed}')
            coor_byte = '{val_x},{val_y}'.format(val_x=self.val_x,val_y=self.val_y)
            coor_byte = bytes(coor_byte,encoding='utf8')
            print(coor_byte)
            client_socket.sendto(coor_byte,addr)

        except socket.timeout:
            print('REQUEST TIMED OUT')




            
 