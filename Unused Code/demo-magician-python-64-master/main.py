import DobotDllType as dType

class Main:

    def __init__(self):
        self.api = dType.load()
        dType.ConnectDobot(self.api, "", 115200)
        STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
        MM_PER_CRICLE = 3.1415926535898 * 36.0
        self.vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE
        current_pose = dType.GetPose(self.api)
        (self.X,self.Y,self.Z,self.R,self.R1,self.R2,self.R3,self.R4)=current_pose

        dType.SetHOMEParams(self.api, 200, 200, 200, 200, isQueued = 1)
        dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)
        
    


    def conveyor(self,on_state):
        if on_state == True:
            dType.SetEMotorEx(self.api, 0, 1, int(self.vel), 1)
        elif on_state == False:
            dType.SetEMotorEx(self.api, 0, 1, 0, 1)




    #dType.SetEndEffectorSuctionCup(api, True, False, False)
    def arm_move(self,X_off,Y_off,Z_off):
        dType.SetPTPCmd(self.api,dType.PTPMode.PTPMOVLXYZMode, self.X+X_off, self.Y+Y_off, self.Z+Z_off, self.R, isQueued = 1)

    def disconnect(self):
        dType.DisconnectDobot


test = Main()

#test.conveyor(True)
#test.arm_move(0,0,-20)
test.conveyor(False)