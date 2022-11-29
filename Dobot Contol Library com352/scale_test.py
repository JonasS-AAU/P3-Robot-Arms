import commands
from communication import Commmunication as coms
from camera import Camera as cam

cmds = commands.Commands("PORT")

cmds.home()

img1 = cam.capture_image()
cam.save_image(img1,"first_img")
cmds.move_relaive(20,0,0)
img2 = cam.capture_image()
cam.save_image(img2,"last_img")

