#Importing used libraries and classes
import lib.commands as cmds
from lib.Colour_check import clr_rec
from Server_client.client import Client
from picamera import PiCamera
from gpiozero import LED, Button
from signal import pause
import time
import numpy as np

#Function that resets the dobots position
def startup():
    cmd.home()

#Function that gets the first cube's coordinates 
def getcoords(img,color_index):
    #Scans the given image for colors of cubes other than the one given
    lis = col.find_outlier(img,color_index,boundaries,20)

    #Prints list to show what cubes have been found, and then returns the first cube's coordinates
    print(lis)
    (x,y) = lis[0]
    return x,y

#Moves the arm back to its start position
def move_arm_start():
    cmd.move_arm(cmd.home_coord[0],cmd.home_coord[1],cmd.home_coord[2])

#Removes the block from the conveyor belt
def remove_block(pos_y, conveyor_dist):
    #Calculates the position the arm needs to move to
    d_y = (pos_y - 96)*((pos_y-conveyor_dist)*0.0012+0.57)

    #Sequence that moves to position, picks up cube and then returns to the start to drop the cube
    cmd.move_arm(cmd.home_coord[0]+d_y,cmd.home_coord[1],cmd.home_coord[2])
    time.sleep(1)
    cmd.move_arm(cmd.home_coord[0]+d_y,cmd.home_coord[1],cmd.home_coord[2]-30)
    time.sleep(1)
    cmd.enable_suction(1)
    time.sleep(1)
    cmd.move_arm(cmd.home_coord[0]+d_y,cmd.home_coord[1],cmd.home_coord[2])
    cmd.move_arm(cmd.home_coord[0],cmd.home_coord[1],cmd.home_coord[2])
    time.sleep(2)
    cmd.enable_suction(0)

#Starts or stops the conveyer depending on the parameter given
def move_conveyor(state):
    if state == True:
        cmd.set_conveyor_speed(-1500)
    if state == False:
        cmd.set_conveyor_speed(0)

#Button functions
#A function to start the program in case it has been stopped. Resumes in the movement it was executing.
def program_on():
    global running
    running = True
    cmd.res()

#A function to stop the program in case it has been started. Stops the arm in the movement it is executing.
def program_off():
    global running 
    running = False
    move_conveyor(0)
    cmd.death()

# A class to handle the lights and the button controlling the lights
class Lights:
    def __init__(self,buttonGPIO,lightsGPIO):
        '''
        A class that handles the lights that represents which cubes to ignore.
        
        :params buttonGPIO: The connected GPIO of the button that switches through the lights
        :params lightsGPIO: A list of all the GPIO used by lights that need to be connected. Input needs to be sorted the way lights are changed.
        '''
        i = 0
        self.lights = []
        self.button = Button(buttonGPIO)                #Creates a button using the GPIOZero library
        
        #Creates lights using the GPIOZero library, and adds them to a list
        for i in range(len(lightsGPIO)):
            self.lights.append(LED(lightsGPIO[i]))
        self.lights[0].on()
        
    #Function to determine what happens when pressing the switch
    def light_shift(self):
        #Global variables to change what to sort for
        global color_keep
        global light
        
        #Turning off previous light and turns on next light. Also changes what color of cubes to keep, depending on the light turned on.
        if light == 0:
            self.lights[len(self.lights)-1].off()
            self.lights[light].on()
            color_keep = 0
            light = light +1
        elif light == 1:
            self.lights[light-1].off()
            self.lights[light].on()
            light = light +1
            color_keep = 1
        elif light  == 2:
            self.lights[light-1].off()
            self.lights[light].on()
            light = 0
            color_keep = 2

#Main program
def run(arm_pos,speed):
    #Takes a picture and scans it to determine where the beginning of the conveyor belt is.
    camera.capture("/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg")
    img = "/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg"
    conveyor_start = col.find_start_px(img,480)

    #Main loop
    while True:
        #Try function to enable button presses and switches
        try:
            gpio.button.when_pressed = gpio.light_shift
            switch_on.when_pressed = program_on
            switch_off.when_pressed = program_off

            #While loop handling the execution of the program, can be stopped by flipping the switch.
            while running == True:
                
                #Starts by starting the conveyor belt.
                move_conveyor(1)

                #Takes picture to scan and starts taking time
                camera.capture("/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg")
                start = time.time()
                img = "/media/comtek3/USB DISK/Dobot Contol Library com352/server_img.jpg"

                #Checks if there are any found cubes in the picture. If not, prints "No cube"
                try:
                    pos_x,pos_y = getcoords(img,color_keep)

                    #Finds the time it took to scans picture
                    time_taken = start - time.time()
                    
                    #Checks if the cube moved into the arms range while processing the image. 
                    #If it did, turns off conveyor, removes cube and starts conveyor again.
                    #Also prints "Found cube"
                    if arm_pos > (pos_x-(speed*time_taken)):
                        move_conveyor(0)
                        remove_block(pos_y, conveyor_start)
                        move_conveyor(1)
                    print("Found cube")
                except:
                    print("No cube")
                    pass

        finally:
            pass

#Defining the values of variables used in the program
center_arm = 440                            #The place on the x-axis of the picture that the arms center is
speed = 13                                  #The speed of the conveyor belt
SERVER_IP = "192.168.1.59"                  #Server IP for the client
SERVER_PORT = 8888                          #Server PORT for the client
BUFFER_SIZE = 2048                          #Server buffer_size for the client
light = 1                                   #What light is gonna turn on when the button is pressed
running = True                              #If the program is running
color_keep = 0                              #What color to keep (The index of the boundaries list)
boundaries = [                              #List of color boundaries, defined with a lower and upper boundary for each color
	([17, 15, 100], [50, 56, 200]),         #Red color
	([86, 31, 4], [220, 88, 50]),           #Blue color
	([25, 146, 190], [62, 250, 255]),       #Yellow color
]
lightgpio = [26,19,13]                      #List of GPIO ports used for lights

#Creating objects of the different classes used in the program
cmd = cmds.Commands("/dev/ttyUSB0")         #Creating the command object with the parameter being the usb port connected to a turned on dobot
col = clr_rec(center_arm)                   #Creating the color recognition object with the arms center as parameter                      
gpio = Lights(21,lightgpio)                 #Creating lights and button object
camera = PiCamera()                         #Creating Pi camera object
c = Client(SERVER_IP, SERVER_PORT, BUFFER_SIZE) #Creates client
switch_on = Button(5)                       #Creates on switch object
switch_off = Button(6)                      #Creates off switch object


#startup()                                  #Run first time dobot is turned on, and when dobot is removed from power, Comment out afterwards
#move_arm_start()                           #Run AFTER running the program calling the startup function, Comment out afterwards
#run(center_arm,speed)                      #Run when running the program
move_conveyor(1)                           #Run if conveyor is not turned off after commenting run function


#camera.capture("/media/comtek3/USB DISK/Dobot Contol Library com352/test1.jpg")
#img = "/media/comtek3/USB DISK/Dobot Contol Library com352/test1.jpg"
#col.find_start_px(img,480)
#c.connect_send(img)
