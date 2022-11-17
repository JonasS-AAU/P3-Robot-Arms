import communication 

class Dobot:
    def __init__(self,port):
        self.port = port
        self.coms = communication.Communication()
        self.serial = self.coms.setup_serial(self.port)
        # replace "COM4" with usb port dobot is connected to
        self.command_id = {
            
            "SUCK": 63,
            "MOVE": 84,
            "CONVEYOR": 135

        }

    def toggle_suck(self, state):
        msg = self.coms.build_messag(self.command_id["SUCK"], 3, [state,0])
        self.coms.send_command(self.serial,msg)

    def move_arm(self, x, y, z, r ):
        msg = self.coms.build_messag(self.command_id["MOVE"], 3, [2, x, y, z, r])
        self.coms.send_command(self.serial,msg)

    def move_conveyor(self, speed): 
        msg = self.coms.build_messag(self.command_id["CONVEYOR"], 3, [0, 1, speed])
        print(msg)
        self.coms.send_command(self.serial,msg)

dobot = Dobot("COM4")

dobot.move_conveyor(8)

