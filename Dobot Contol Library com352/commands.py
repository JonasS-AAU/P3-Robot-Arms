from communication import Commmunication as coms
import serial as ser
import struct

class Commands:
    def __init__(self,port):
        self.serial_port = coms.setup_serial(self,port)

    def set_conveyor_speed(self,speed):
        '''
        Activates the stepper motor connected to Dobot stepper_1

        :param speed: float value for speed of stepper motor
        '''
        payload = coms.pack_payload(coms,'=BBBBi', 135,3,0,1,speed)
        length = coms.calculate_length(coms,'=BBBBi')
        checksum = coms.calculate_checksum(coms,list(payload))
        print(checksum)
        command = coms.build_command(coms,payload,length,checksum)
        coms.send_command(coms,self.serial_port,command)


    def home(self): 
        '''
        Returns arm to default home position
        '''
        payload = coms.pack_payload(coms, '=BBi', 31, 3, 0)
        length = coms.calculate_length(coms,'=BBi')
        checksum = coms.calculate_checksum(coms,list(payload))
        command = coms.build_command(coms,payload,length,checksum)
        coms.send_command(coms,self.serial_port,command)


    def enable_suction(self,enabled):
        '''
        Enables suction cup addon

        :param enabled: boolean for state of suction cup (enabled if True)
        '''
        payload = coms.pack_payload(coms, '=BBBB', 62, 3, enabled, 1)
        length = coms.calculate_length(coms, '=BBBB')
        checksum = coms.calculate_checksum(coms,list(payload))
        command = coms.build_command(coms,payload,length,checksum) 
        coms.send_command(coms,self.serial_port,command)

    

    def move_arm(self,x,y,z):
        '''
        moves arm to position

        :param x: float x position in cartesian plane
        :param y: float y position in cartesian plane
        :param z: float z position in cartesian plane
        '''
        payload = coms.pack_payload(coms, '=BBBffff',84,3,2,x,y,z,0)
        length = coms.calculate_length(coms, '=BBBffff')
        checksum = coms.calculate_checksum(coms, list(payload))
        command = coms.build_command(coms,payload,length,checksum)
        coms.send_command(coms,self.serial_port,command)


    def get_pose(self):
        '''
        requests current pose from dobot
        '''
        payload = coms.pack_payload(coms,'=BB',10,0)
        length = coms.calculate_length(coms, '=BB')
        checksum = coms.calculate_checksum(coms, list(payload))
        command = coms.build_command(coms,payload,length,checksum)
        coms.send_command(coms,self.serial_port,command)


    def read_pose(self):
        '''
        calls get_pose() then reads and parses response
        '''
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

    def move_relaive(self,delta_x,delta_y,delta_z):
        (x,y,z) = self.read_pose
        self.move_arm(x+delta_x,y+delta_y,z+delta_z)
        


cmds = Commands("COM3")



    