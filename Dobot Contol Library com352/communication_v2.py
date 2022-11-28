import struct
import serial

class Commmunication:
    def __init__(self):

        pass

    def setup_serial(self,port):
        serail_port = serial.Serial(
            port = port,
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS
        )
        return serail_port

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

'''
coms = Commmunication
ser = coms.setup_serial(coms,'COM4')

def set_conveyor_speed(speed):
    payload = coms.pack_payload(coms,'=BBBBi', 135,3,0,1,speed)
    length = coms.calculate_length(coms,'=BBBBi')
    checksum = coms.calculate_checksum(coms,list(payload))
    print(checksum)
    command = coms.build_command(coms,payload,length,checksum)
    return command

def home(): 
    payload = coms.pack_payload(coms, '=BBi', 31, 3, 0)
    length = coms.calculate_length(coms,'=BBi')
    checksum = coms.calculate_checksum(coms,list(payload))
    command = coms.build_command(coms,payload,length,checksum)
    return command

def enable_suction(enabled):
    payload = coms.pack_payload(coms, '=BBBB', 62, 3, enabled, 1)
    length = coms.calculate_length(coms, '=BBBB')
    checksum = coms.calculate_checksum(coms,list(payload))
    command = coms.build_command(coms,payload,length,checksum) 
    return command

def move_arm(x,y,z):
    payload = coms.pack_payload(coms, '=BBBffff',84,3,2,x,y,z,0)
    length = coms.calculate_length(coms, '=BBBffff')
    checksum = coms.calculate_checksum(coms, list(payload))
    command = coms.build_command(coms,payload,length,checksum)
    return command

def get_pose():
    payload = coms.pack_payload(coms,'=BB',10,0)
    length = coms.calculate_length(coms, '=BB')
    checksum = coms.calculate_checksum(coms, list(payload))
    command = coms.build_command(coms,payload,length,checksum)
    return command

def read_pose():

    wrapraw =ser.read(5)
    wrapper = struct.unpack('=BBBBB',wrapraw)
    print(wrapper)
    poseraw = ser.read(20)
    pose = struct.unpack('=fffff',poseraw)
    print(pose)
    (x,y,z,r,ja) = pose
    return x,y,z
    

command = get_pose()
#command = move_arm(0,0,50)
print(command)
ser.write(command)
ser.flush
#response = ser.read()
print()
x,y,z = read_pose()
print(x,y,z)

command2 =move_arm(x,y,z+20)
ser.write(command2)

#REMEMBER TO MAKE RELATIVE NOT ABSOLUTE BY PUTTING GET POSE INTO MOVE ARM COMMAND

'''

    

