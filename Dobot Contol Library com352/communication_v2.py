import struct
import serial as ser

class Commmunication:
    def __init__(self):

        pass

    def setup_serial(self,port):
        serial_port = ser.Serial(
            port = port,
            baudrate = 115200,
            parity = ser.PARITY_NONE,
            stopbits = ser.STOPBITS_ONE,
            bytesize = ser.EIGHTBITS
        )
        return serial_port

    def pack_payload(self, format,*args):
        b_array = struct.pack(format,*args)
        return b_array

    def calculate_length(self,format):
        len = struct.calcsize(format)
        return len

    def calculate_checksum(self,*payload):
        sum_payload = sum(*payload)
        checksum = (256 - (sum_payload % 256) % 256)
        return checksum

    def build_command(self,packaged_payload,length,checksum):
        packaged_length = struct.pack('B',length)
        packaged_checksum = struct.pack('B',checksum)
        packaged_header = struct.pack('BB',170,170)   
    
        command = packaged_header + packaged_length + packaged_payload + packaged_checksum

        return command
    

    def send_command(self,ser,command):
        ser.write(command)
    


