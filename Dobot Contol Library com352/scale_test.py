import commands
from communication import Commmunication as coms
from camera import Camera as cam

cmds = commands.Commands("PORT")

cmds.move_arm(cmds.home_coord[0],cmds.home_coord[1],cmds.home_coord[2])
img = cam.capture_image()

cam.save_image(img,'')

