import serial

class Communication:
    def __init__(self):

        pass

    def setup_serial(self, port):
        Serial = serial.Serial(
            port = port,
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS
        )
        return Serial

    def parse(self, msg):
        bytes = list(msg)
        
        header = bytes[0:2]
        length = bytes[2]
        id = bytes[3]
        control = bytes[4]
        rw = (control & 1) == 1
        is_q = ((control & 2) >> 1) == 1
        params = bytes[5:-1]
        #checksum not in use, all messages assumed verified
        #checksum = bytes[-1]

        return(header,length,id,rw,is_q,params)
    '''
    def read(self, serial):
        # header not currently used but can be used to verify that correct format is recieved
        header = serial.read(2)
        length = int.from_bytes(serial.read,'little')
        payload = serial.read(length)
        checksum = serial.read(1)

        return (self.parse(header + bytes([length])+ payload + checksum))
    '''
    def send_command(self, Serial, msg):
        print(Serial.isOpen)
        Serial.write(msg)
        Serial.flush
        #(rHeader,rLength,rId,rRW,rIsQueued,rParams) = self.read(Serial)
        #print(rParams)
        #return (rHeader,rLength,rId,rRW,rIsQueued,rParams)

    def calculate_checksum(self, id, control, params):
        payload = id + control
        for i in range(len(params)):
            payload = payload + params[i]

        x = payload % 256
        checksum = (256-x) % 256
        return checksum

    def calculate_length(self, params):
        length = 2 + len(params)
        return length

    def build_messag(self, id, control, params):
        checksum = self.calculate_checksum(id, control, params)
        length = self.calculate_length(params)
        msg = bytes([0xAA, 0xAA] + [length] + [id] + [control] + params + [checksum])
        return msg




#make dict to store id
#make function to calculate control byte from rw and isQ

        
