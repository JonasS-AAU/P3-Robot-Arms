import lib.commands as cmds
from time import sleep,time
from lib.Colour_check import clr_rec as cc
import numpy as np


cmd = cmds.Commands("COM4")
col = cc()
upper = np.array([50, 56, 200])
lower = np.array([17, 15, 100])
def startup():
    cmd.home()


    
def getcoords(img):
    start = time()
    a,b = col.find_clr(img,upper,lower)

    lis = col.find_coordinates(a,b,10)
    stop = time()

    print (start - stop)
    (x,y) = lis[0]
    return x,y

def move_arm_start():
    cmd.move_arm(cmd.home_coord[0],cmd.home_coord[1],cmd.home_coord[2])

def remove_block():
    img = "Server_client\server_img.jpg"

    pos_x,pos_y = getcoords(img)

    print(pos_x)
    print(pos_y)

    if pos_y < 190:
        d_y = (pos_y - 96)*0.50
    elif pos_y > 230:
        d_y = (pos_y - 96)*0.65
    else:
        d_y = (pos_y - 96)*0.60

    cmd.move_arm(cmd.home_coord[0]+d_y,cmd.home_coord[1],cmd.home_coord[2])
    sleep(1)
    cmd.move_arm(cmd.home_coord[0]+d_y,cmd.home_coord[1],cmd.home_coord[2]-30)
    sleep(1)
    cmd.enable_suction(1)
    sleep(1)
    cmd.move_arm(cmd.home_coord[0]+d_y,cmd.home_coord[1],cmd.home_coord[2])
    cmd.move_arm(cmd.home_coord[0],cmd.home_coord[1],cmd.home_coord[2])
    sleep(2)
    cmd.enable_suction(0)

remove_block()
