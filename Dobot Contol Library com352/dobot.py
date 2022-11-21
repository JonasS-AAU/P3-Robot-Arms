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
        msg = self.coms.build_messag(self.command_id["MOVE"], 3, [0x02, x, y, z, r])
        self.coms.send_command(self.serial,msg)

    def move_conveyor(self, enabled):
        if enabled == True:
            msg = bytes([0xAA]+ [0xAA] + [0x08] + [0x87] + [0x03] + [0x00] + [0x01] + [0xF0] + [0xD8] + [0xFF] + [0xFF] + [0xAF])
        elif enabled == False:
            msg = self.coms.build_messag(self.command_id["CONVEYOR"], 3, [0, 1, 0])

        self.coms.send_command(self.serial,msg)

    def send_raw_command(self,hex_string):
        msg = bytes(hex_string)
        self.coms.send_command(self.serial, msg)
    

dobot = Dobot("COM4")

# set acc comands to 50 50 50 50
dobot.send_raw_command([0xAA]+[0xAA]+[0x12]+[0x51]+[0x03]+  [0x42]+[0x48]+[0x00]+[0x00]+  [0x42]+[0x48]+[0x00]+[0x00]+  [0x42]+[0x48]+[0x00]+[0x00]+  [0x42]+[0x48]+[0x00]+[0x00] + [0x84])
# set common commands to 50 50
dobot.send_raw_command([0xAA]+[0xAA]+[0x0A]+[0x53]+[0x03]+  [0x42]+[0x48]+[0x00]+[0x00]+  [0x42]+[0x48]+[0x00]+[0x00]+ [0x96])
# move to 100 100 100 0
dobot.send_raw_command([0xAA]+[0xAA]+[0x13]+[0x54]+[0x03]+  [0x42]+[0xC8]+[0x00]+[0x00]+  [0x42]+[0xC8]+[0x00]+[0x00]+  [0x42]+[0xC8]+[0x00]+[0x00]+  [0x00]+[0x00]+[0x00]+[0x00]+ [0x89])


