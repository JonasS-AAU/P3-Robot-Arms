import DobotDllType as dType

api = dType.load()
dType.ConnectDobot(api, "", 115200)

STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
MM_PER_CRICLE = 3.1415926535898 * 36.0
vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE

dType.SetEMotorEx(api, 0, 1, int(vel), 1)
current_pose = dType.GetPose(api)
(X,Y,Z,R,R1,R2,R3,R4)=current_pose 
dType.SetEndEffectorSuctionCup(api, True, True, False)

#dType.SetHomeParams(api, 250, 0, 50, 0, isQueued = 1)
dType.SetPTPCmd(api,dType.PTPMode.PTPMOVLXYZMode, X, Y, Z+20, R, isQueued = 1)