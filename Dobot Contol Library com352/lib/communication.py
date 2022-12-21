import struct
import serial as ser

class Commmunication:
    def __init__(self):

        pass

    def setup_serial(self,port):
        """
        This function sets up a serial connection over USB with the given paramenters.
        
        :param port: USB the serial connection should be established over
        """
        serial_port = ser.Serial(
            port = port,
            baudrate = 115200,
            parity = ser.PARITY_NONE,
            stopbits = ser.STOPBITS_ONE,
            bytesize = ser.EIGHTBITS
        )
        return serial_port

    def pack_payload(self, format,*args):
        """
        This functions uses struct.pack to convert a format string and a list of parameters into a byte_string
        
        :param format: the format of the paramters to be packed, syntax can be found in struct documentation
        :param *args: list of parameters to be packed
        """
        b_array = struct.pack(format,*args)
        return b_array

    def calculate_length(self,format):
        """
        This function finds the length of the payload
        
        :param format: the format of the payload, syntax can be found in struct documentation
        """
        len = struct.calcsize(format)
        return len

    def calculate_checksum(self,*payload):
        """
        This function finds the checksum of a payload parmater list
        
        :param *payload: list of payload paramters
        """
        sum_payload = sum(*payload)
        checksum = (256 - (sum_payload % 256) % 256)
        return checksum

    def build_command(self,packaged_payload,length,checksum):
        """
        This function packs the final byste-string for the command to be sent
        
        :param packaged_payload: the packaged packload that is returned by pack_payload()
        :param length: the length of the payload returned by calculate_length()
        :param checksum: the checksum of the payload returned by calculate_checksum()
        """
        packaged_length = struct.pack('B',length)
        packaged_checksum = struct.pack('B',checksum)
        packaged_header = struct.pack('BB',170,170)   
    
        command = packaged_header + packaged_length + packaged_payload + packaged_checksum

        return command
    

    def send_command(self,ser,command):
        """
        This function sends a command through the serial connection created by setup_serial()
        
        :param commmand: the byte-string of a command retuned by build_command()
        """
        ser.write(command)
    


