from serial.tools import list_ports
import pydobot
from time import sleep
import keyboard

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device
device = pydobot.Dobot(port=port,verbose=True)

(x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()

print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

device.move_to(x,y,z+50,r, wait = True)
acc = 50
while True:
    if keyboard.read_key() == "w":
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
        device.move_to(x+acc,y,z,r, wait = True)
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
    elif keyboard.read_key() == "s":
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
        device.move_to(x-acc,y,z,r, wait = True)
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
    elif keyboard.read_key() == "a":
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
        device.move_to(x,y+acc,z,r, wait = True)
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
    elif keyboard.read_key() == "d":
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
        device.move_to(x,y-acc,z,r, wait = True)
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
    elif keyboard.read_key() == "r":
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
        device.move_to(x,y,z+acc,r, wait = True)
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
    elif keyboard.read_key() == "f":
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
        device.move_to(x,y,z-acc,r, wait = True)
        (x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()
    elif keyboard.read_key() == "q":
        device.suck(True)
    elif keyboard.read_key() == "e":
        device.suck(False)
    elif keyboard.read_key() == "h":
        break
(x ,y ,z ,r ,j1 ,j2 ,j3 ,j4) = device.pose()

device.close