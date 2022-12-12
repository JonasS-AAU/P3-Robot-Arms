import lib.commands as cmds
from time import sleep,time
from lib.Colour_check import clr_rec as cc
import numpy as np
from lib.camera import Camera as cam

cmd = cmds.Commands("COM4")
col = cc()
upper = np.array([50, 56, 200])
lower = np.array([17, 15, 100])
boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 250, 255])
]

def startup():
    cmd.home()


    
def getcoords(img):
    start = time()
    lis = col.find_outlier(img,0,boundaries,10)

    stop = time()

    print (start - stop)
    print(lis)
    (x,y) = lis[0]
    return x,y

def move_arm_start():
    cmd.move_arm(cmd.home_coord[0],cmd.home_coord[1],cmd.home_coord[2])

def remove_block(pos_y):

    d_y = (pos_y - 96)*((pos_y-160)*0.00071428571+0.6)

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

def move_conveyor(state):
    if state == True:
        cmd.set_conveyor_speed(-2500)
    if state == False:
        cmd.set_conveyor_speed(0)

def run():
    move_conveyor(1)
    camera = cam()
    while 28 == 28:
            raw_img = camera.capture_image()
            camera.save_image(raw_img,"Server_client\server_img.jpg")
            img = "Server_client\server_img.jpg"
            try:
                pos_x,pos_y = getcoords(img)
                if 408 < pos_x:
                    move_conveyor(0)
                    remove_block(pos_y)
                    move_conveyor(1)

            except:
                pass
