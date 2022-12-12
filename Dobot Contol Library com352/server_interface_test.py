import lib.commands as cmds
from time import sleep,time
from lib.Colour_check import clr_rec as cc
import numpy as np
from Server_client.client import Client
#from lib.camera import Camera as cam
from picamera import PiCamera

cmd = cmds.Commands("/dev/ttyUSB0")
col = cc()
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
BUFFER_SIZE = 2048

upper = np.array([50, 56, 200])
lower = np.array([17, 15, 100])
boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 250, 255]),
    ([29,86,6],[64,255,255])
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
        cmd.set_conveyor_speed(-1500)
    if state == False:
        cmd.set_conveyor_speed(0)

def run():
    move_conveyor(1)
    while 28 == 28:
        camera.capture("/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg")
        #camera.save_image(raw_img,"/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg")
        img = "/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg"
        try:
            pos_x,pos_y = getcoords(img)
            if 450 > pos_x and 160 < pos_y:
                move_conveyor(0)
                remove_block(pos_y)
                move_conveyor(1)
            print("found cube")
        except:
            print("No cube")
            pass
camera = PiCamera()
camera.capture("/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg")
#camera.save_image(raw_img,"/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg")
img = "/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg"
c = Client(SERVER_IP, SERVER_PORT, BUFFER_SIZE)
#run()
c.connect_send(img)
move_conveyor(0)