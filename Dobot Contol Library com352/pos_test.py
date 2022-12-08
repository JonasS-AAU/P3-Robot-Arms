import lib.commands as cmds
#from lib.camera import Camera as cam
#from lib.Colour_check import clr_rec as cc
from time import sleep

cmd = cmds.Commands("COM3")

a = (500 - 405)
b = (300 - 249)


def test():
    cmd.move_arm(cmd.home_coord[0],cmd.home_coord[1],cmd.home_coord[2])
    sleep(5)
    #cmd.move_arm(cmd.home_coord[0]+a,cmd.home_coord[1]+b,cmd.home_coord[2])

def startup():
    cmd.home()

def test2():
    print(cmd.home_coord[0])
    print(cmd.home_coord[1])
    print(cmd.home_coord[2])

def test3():
    cmd.move_arm(150.0,0.0,0.0)

test3()
#startup()
#pseudocode for 