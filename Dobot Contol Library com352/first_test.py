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
a,b = cc.find_coordinates(cc,x,y)

c1 = (a - 405)*1.1
c2 = (b - 249)*1.1
c3 = 5

cmds.move_arm(c1,c2,cmds.home_coord[2])
time.sleep(5)
cmds.move_arm(c1,c2,c3)
time.sleep(5)
cmds.enable_suction(1)
time.sleep(5)
cmds.move_arm(cmds.home_coord[0],cmds.home_coord[1],cmds.home_coord[2])
time.sleep(5)
cmds.enable_suction(0)



cmds.mo
