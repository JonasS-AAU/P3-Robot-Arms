from signal import pause
from gpiozero import LED, Button
import time
leds = []
light= 0
color_keep = 0
'''
button = Button(21)
led_yellow = LED(26)
led_red = LED(19)
led_blue = LED(13)
led_yellow.off()
'''
class Lights:
    def __init__(self,buttonGPIO,lightsGPIO):
        i = 0
        self.lights = []
        self.button = Button(buttonGPIO)
        for i in range(len(lightsGPIO)):
            self.lights.append(LED(lightsGPIO[i]))
        self.lights[0].on()
        

    def light_shift(self):
        global color_keep
        global light
        
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

#lightgpio = [26,19,13]
#gpio = Lights(21,lightgpio)

'''
try:
    gpio.button.when_pressed = gpio.light_shift

    while True:
        print(color_keep)
        time.sleep(5)

    pause()


finally:
    pass
'''