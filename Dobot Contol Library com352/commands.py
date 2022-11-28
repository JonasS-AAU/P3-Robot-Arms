from communication_v2 import Commmunication as coms
import serial as ser
import struct

class Commands:
    def __init__(self,port):
        coms.setup_serial(self,port)

def set_conveyor_speed(self,speed):
    payload = coms.pack_payload(coms,'=BBBBi', 135,3,0,1,speed)
    length = coms.calculate_length(coms,'=BBBBi')
    checksum = coms.calculate_checksum(coms,list(payload))
    print(checksum)
    command = coms.build_command(coms,payload,length,checksum)
    return command

def home(self): 
    payload = coms.pack_payload(coms, '=BBi', 31, 3, 0)
    length = coms.calculate_length(coms,'=BBi')
    checksum = coms.calculate_checksum(coms,list(payload))
    command = coms.build_command(coms,payload,length,checksum)
    return command

def enable_suction(self,enabled):
    payload = coms.pack_payload(coms, '=BBBB', 62, 3, enabled, 1)
    length = coms.calculate_length(coms, '=BBBB')
    checksum = coms.calculate_checksum(coms,list(payload))
    command = coms.build_command(coms,payload,length,checksum) 
    return command

def move_arm(self,x,y,z):
    payload = coms.pack_payload(coms, '=BBBffff',84,3,2,x,y,z,0)
    length = coms.calculate_length(coms, '=BBBffff')
    checksum = coms.calculate_checksum(coms, list(payload))
    command = coms.build_command(coms,payload,length,checksum)
    return command

def get_pose(self):
    payload = coms.pack_payload(coms,'=BB',10,0)
    length = coms.calculate_length(coms, '=BB')
    checksum = coms.calculate_checksum(coms, list(payload))
    command = coms.build_command(coms,payload,length,checksum)
    return command

def read_pose(self):
    ser.flush()
    self.get_pose()
    wrap_raw = ser.read(5)
    wrapper = struct.unpack('=BBBBB',wrap_raw)
    print(wrapper)
    pose_raw = ser.read(20)
    pose = struct.unpack('=fffff',pose_raw)
    print(pose)
    #rotation and joint angle not currently in use
    (x,y,z,r,j_angle) = pose
    return x,y,z
        


cmds = Commands("COM4")

    
    