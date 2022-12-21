from communication import Commmunication as coms
import commands
from camera import Camera as cam
import numpy as np
from Colour_check import clr_rec as cc
import time

cmds = commands.Commands('port')

upper = np.array([50, 56, 200])
lower = np.array([17, 15, 100])

cmds.move_arm(cmds.home_coord[0],cmds.home_coord[1],cmds.home_coord[2])

img = cam.capture_image()

x,y = cc.find_clr(cc,img,upper,lower)
center_list = cc.find_coordinates(cc,x,y)
(x,y) = center_list [0]

c1 = (x - 405)
c2 = (y - 249)
c3 = 5

cmds.move_relaive(c1,c2,cmds.home_coord[2])
time.sleep(5)
cmds.move_relaive(0,0,-10)
time.sleep(5)
cmds.enable_suction(1)
time.sleep(5)
cmds.move_arm(cmds.home_coord[0],cmds.home_coord[1],cmds.home_coord[2])
time.sleep(5)
cmds.enable_suction(0)

