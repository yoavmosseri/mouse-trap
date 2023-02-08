import threading
import mouse
import math
import sys
from pyautogui import size
from dot import Dot
from time import sleep, time
from SQL_ORM import DotORM

COLLECTING_DATA = False
db = DotORM()

def shrink(dot: tuple, resolution: tuple):
    """
    adjust the resolution to 1920*1080.
    input:  dot is tuple x and y
            resolution is the screen current resolution
    output: tuple (x,y) out of 1920*1080 screen.
    """
    shrinked_x = (dot[0] / resolution[0]) * 1920
    shrinked_y = (dot[1] / resolution[1]) * 1080

    return (int(shrinked_x), int(shrinked_y))


def get_position():
    loc = mouse.get_position()
    return shrink(loc, size())


def calc_velocity(prev_loc, next_loc, delta_t):
    return math.sqrt(math.pow(next_loc[0]-prev_loc[0], 2)+math.pow(next_loc[1]-prev_loc[1], 2)) / delta_t


def collect_data(username):
    global COLLECTING_DATA
    """
    we will collect raw data every 0.01 second. 
    every 10 dots we will average them to one dot, and add it to the return list.
    
    input is when to stop by COLLECTING_DATA and username to save
    every 10 seconds will save progress
    """
    COLLECTING_DATA = True
    period = 10
    data = []
    prev_loc = get_position()
    prev_time = time()
    while COLLECTING_DATA:
        temp_dot = Dot(0,0,0)
        for j in range(period): # ten seconds
            sleep(0.01)
            next_loc = get_position()
            next_time = time()

            temp_dot.x += next_loc[0]
            temp_dot.y += next_loc[1]
            temp_dot.v += calc_velocity(prev_loc,next_loc,next_time-prev_time)

            prev_loc = next_loc
            prev_time = next_time
        
        temp_dot.x = int(temp_dot.x / period)
        temp_dot.y = int(temp_dot.y / period)
        temp_dot.v /= period

        data.append(temp_dot)

        if len(data) % 100 == 0:
            save_data(data, username)
            data.clear()
        
        print('collecting data',COLLECTING_DATA)
            
    save_data(data,username)

    print('done')
    return True


def save_data(data: list, username):
    global db
    for dot in data:
        db.insert_dot(username, dot)
    
    return True


def stop():
    global COLLECTING_DATA
    COLLECTING_DATA = False

"""
t = threading.Thread(target= collect_data,args=(sys.argv[1],))
t.start()

while True:
    a = input("enter a: ")
    if a == 'a':
        COLLECTING_DATA = False
        print('bye')
        break
"""

