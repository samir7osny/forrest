from CoM.motor import *
from CoM.obj import *

HandLPIN =  3
HandLZERO =  1500
ArmLPIN =  2
ArmLZERO =  1500
ShoulderLPIN =  1
ShoulderLZERO =  1500

HandRPIN =  30
HandRZERO =  1500
ArmRPIN =  31
ArmRZERO =  1500
ShoulderRPIN =  32
ShoulderRZERO =  1500

FootLPIN =  12
FootLZERO =  1550
AnkleLPIN =  11
AnkleLZERO =  1500
KneeLPIN =  10
KneeLZERO =  1500
LegLPIN =  9
LegLZERO =  1550
HipLPIN =  8
HipLZERO =  1450

FootRPIN =  21
FootRZERO =  1500
AnkleRPIN =  22
AnkleRZERO =  1400
KneeRPIN =  23
KneeRZERO =  1600
LegRPIN =  24
LegRZERO =  1450
HipRPIN =  25
HipRZERO =  1500

HeadPIN =  17
HeadZERO =  1500

PinsPerAngle = (2500 - 500) // 180

class Robot(Obj):
    def __init__(self):

        self.MotorXSize = 20
        self.MotorYSize = 40
        self.MotorZSize = 40.5

        self.MotorPZAxis = 9
        self.MotorNZAxis = self.MotorZSize - self.MotorPZAxis
        self.MotorCenterToAxis = self.MotorZSize / 2 - self.MotorPZAxis

        self.HipToHip = (67 - 2 * self.MotorCenterToAxis)
        self.HipToShoulder = (104 - self.MotorCenterToAxis)
        self.HipToHead = (109 - self.MotorCenterToAxis)
        self.ShoulderToShoulder = (145 - 2 * (self.MotorYSize/2))
        self.ShoulderToArm = (30 + self.MotorYSize/2)
        self.ArmToHand = (74 - 2* self.MotorCenterToAxis)
        self.HipToLegW = 22
        self.HipToLegH = 39
        self.HipToKnee = (94 - self.MotorCenterToAxis)
        self.LegToKnee = self.HipToKnee - self.HipToLegH
        self.HipToAnkle = (149 - self.MotorCenterToAxis)
        self.KneeToAnkle = self.HipToAnkle - self.HipToKnee
        self.HipToFoot = (197 - self.MotorCenterToAxis)
        self.AnkleToFoot = self.HipToFoot - self.HipToAnkle
        self.FootToGround = 15
        self.HipToGround = self.HipToFoot + self.FootToGround

        self.motor_size = (self.MotorXSize, self.MotorYSize, self.MotorZSize)
        self.motor_rotation_axis_direction = (0, 1, 0)
        self.motor_rotation_axis_position = (0, 0, -self.MotorCenterToAxis)
        self.motor_mass = 64

        const_args = {
            'size': self.motor_size,
            'rotation_axis_direction': self.motor_rotation_axis_direction,
            'rotation_axis_position': self.motor_rotation_axis_position,
            'mass': self.motor_mass
        }

        self.Head = Motor(parent=self, angle_x=0, angle_y=0, angle_z=0, position=(0, 0, self.HipToHead), mode=1, **const_args)

        
        self.ShoulderL = Motor(parent=self, angle_x=0, angle_y=0, angle_z=90, position=(self.ShoulderToShoulder/2, 0, self.HipToShoulder), mode=1, **const_args)
        self.ArmL = Motor(parent=self.ShoulderL, angle_x=0, angle_y=0, angle_z=90, position=(0, -self.ShoulderToArm, 0), **const_args)
        self.HandL = Motor(parent=self.ArmL, angle_x=0, angle_y=180, angle_z=0, position=(0, 0, -self.ArmToHand), mode=1, **const_args)
                
        self.ShoulderR = Motor(parent=self, angle_x=0, angle_y=0, angle_z=-90, position=(-self.ShoulderToShoulder/2, 0, self.HipToShoulder), mode=1, **const_args)
        self.ArmR = Motor(parent=self.ShoulderR, angle_x=0, angle_y=0, angle_z=-90, position=(0, -self.ShoulderToArm, 0), **const_args)
        self.HandR = Motor(parent=self.ArmR, angle_x=0, angle_y=-180, angle_z=0, position=(0, 0, -self.ArmToHand), mode=1, **const_args)
        

        self.HipL = Motor(parent=self, angle_x=0, angle_y=90, angle_z=0, position=(self.HipToHip/2, 0, 0), mode=1, **const_args)
        self.LegL = Motor(parent=self.HipL, angle_x=-90, angle_y=0, angle_z=180, position=(self.HipToLegH, 0, self.HipToLegW), mode=1, **const_args)
        self.KneeL = Motor(parent=self.LegL, angle_x=0, angle_y=-90, angle_z=0, position=(-self.LegToKnee, 0, 0), mode=1, **const_args)
        self.AnkleL = Motor(parent=self.KneeL, angle_x=0, angle_y=0, angle_z=0, position=(0, 0, self.KneeToAnkle), mode=1, **const_args)
        self.FootL = Motor(parent=self.AnkleL, angle_x=0, angle_y=-90, angle_z=-90, position=(0, 0, self.AnkleToFoot), **const_args)

        self.HipR = Motor(parent=self, angle_x=0, angle_y=-90, angle_z=0, position=(-self.HipToHip/2, 0, 0), mode=1, **const_args)
        self.LegR = Motor(parent=self.HipR, angle_x=-90, angle_y=0, angle_z=-180, position=(-self.HipToLegH, 0, self.HipToLegW), mode=1, **const_args)
        self.KneeR = Motor(parent=self.LegR, angle_x=0, angle_y=90, angle_z=0, position=(self.LegToKnee, 0, 0), mode=1, **const_args)
        self.AnkleR = Motor(parent=self.KneeR, angle_x=0, angle_y=0, angle_z=0, position=(0, 0, self.KneeToAnkle), mode=1, **const_args)
        self.FootR = Motor(parent=self.AnkleR, angle_x=0, angle_y=90, angle_z=90, position=(0, 0, self.AnkleToFoot), **const_args)

        self.childs = [self.Head, 
                        self.ShoulderL, self.ArmL, self.HandL,
                        self.ShoulderR, self.ArmR, self.HandR,
                        self.HipL, self.LegL, self.KneeL, self.AnkleL, self.FootL,
                        self.HipR, self.LegR, self.KneeR, self.AnkleR, self.FootR]

        
        self.LastHead=-1
        self.LastShoulderL=-1
        self.LastArmL=-1
        self.LastHandL=-1
        self.LastShoulderR=-1
        self.LastArmR=-1
        self.LastHandR=-1 
        self.LastHipL=-1
        self.LastLegL=-1
        self.LastKneeL=-1
        self.LastAnkleL=-1
        self.LastFootL=-1 
        self.LastHipR=-1
        self.LastLegR=-1
        self.LastKneeR=-1
        self.LastAnkleR=-1
        self.LastFootR=-1

        super().__init__(position=(0, 0, 0))

    def draw(self, ax, Head=0, ShoulderL=0, ArmL=0, HandL=0, ShoulderR=0, ArmR=0, HandR=0 ,HipL=0, LegL=0, KneeL=0, AnkleL=0, FootL=0 ,HipR=0, LegR=0, KneeR=0, AnkleR=0, FootR=0):
        self.Head.rotate(Head) 
        self.ShoulderL.rotate(ShoulderL)
        self.ArmL.rotate(ArmL) 
        self.HandL.rotate(HandL)
        self.ShoulderR.rotate(ShoulderR)
        self.ArmR.rotate(ArmR) 
        self.HandR.rotate(HandR)
        self.HipL.rotate(HipL) 
        self.LegL.rotate(LegL) 
        self.KneeL.rotate(KneeL) 
        self.AnkleL.rotate(AnkleL) 
        self.FootL.rotate(FootL)
        self.HipR.rotate(HipR) 
        self.LegR.rotate(LegR) 
        self.KneeR.rotate(KneeR) 
        self.AnkleR.rotate(AnkleR) 
        self.FootR.rotate(FootR) 
        return super().draw(ax)

    def send_serial(self, ser, Head=0, ShoulderL=0, ArmL=0, HandL=0, ShoulderR=0, ArmR=0, HandR=0 ,HipL=0, LegL=0, KneeL=0, AnkleL=0, FootL=0 ,HipR=0, LegR=0, KneeR=0, AnkleR=0, FootR=0):
        string = ''
        if self.LastHead != Head:
            string = f'#{HeadPIN}P{int(HeadZERO + PinsPerAngle*Head)}'
        if self.LastShoulderL != ShoulderL:
            string += f'#{ShoulderLPIN}P{int(ShoulderLZERO + PinsPerAngle*ShoulderL)}'
        if self.LastArmL != ArmL:
            string += f'#{ArmLPIN}P{int(ArmLZERO + PinsPerAngle*ArmL)}'
        if self.LastHandL != HandL:
            string += f'#{HandLPIN}P{int(HandLZERO + PinsPerAngle*HandL)}'
        if self.LastShoulderR != ShoulderR:
            string += f'#{ShoulderRPIN}P{int(ShoulderRZERO + PinsPerAngle*ShoulderR)}'
        if self.LastArmR != ArmR:
            string += f'#{ArmRPIN}P{int(ArmRZERO + PinsPerAngle*ArmR)}'
        if self.LastHandR != HandR:
            string += f'#{HandRPIN}P{int(HandRZERO + PinsPerAngle*HandR)}'
        if self.LastHipL != HipL:
            string += f'#{HipLPIN}P{int(HipLZERO + PinsPerAngle*HipL)}'
        if self.LastLegL != LegL:
            string += f'#{LegLPIN}P{int(LegLZERO + PinsPerAngle*LegL)}'
        if self.LastKneeL != KneeL:
            string += f'#{KneeLPIN}P{int(KneeLZERO + PinsPerAngle*KneeL)}'
        if self.LastAnkleL != AnkleL:
            string += f'#{AnkleLPIN}P{int(AnkleLZERO + PinsPerAngle*AnkleL)}'
        if self.LastFootL != FootL:
            string += f'#{FootLPIN}P{int(FootLZERO + PinsPerAngle*FootL)}'
        if self.LastHipR != HipR:
            string += f'#{HipRPIN}P{int(HipRZERO + PinsPerAngle*HipR)}'
        if self.LastLegR != LegR:
            string += f'#{LegRPIN}P{int(LegRZERO + PinsPerAngle*LegR)}'
        if self.LastKneeR != KneeR:
            string += f'#{KneeRPIN}P{int(KneeRZERO + PinsPerAngle*KneeR)}'
        if self.LastAnkleR != AnkleR:
            string += f'#{AnkleRPIN}P{int(AnkleRZERO + PinsPerAngle*AnkleR)}'
        if self.LastFootR != FootR:
            string += f'#{FootRPIN}P{int(FootRZERO + PinsPerAngle*FootR)}'
        string = f'{string}T100\r\n'
        print(string)
        ser.write(string.encode())
        
        self.LastHead=Head
        self.LastShoulderL=ShoulderL
        self.LastArmL=ArmL
        self.LastHandL=HandL
        self.LastShoulderR=ShoulderR
        self.LastArmR=ArmR
        self.LastHandR=HandR 
        self.LastHipL=HipL
        self.LastLegL=LegL
        self.LastKneeL=KneeL
        self.LastAnkleL=AnkleL
        self.LastFootL=FootL 
        self.LastHipR=HipR
        self.LastLegR=LegR
        self.LastKneeR=KneeR
        self.LastAnkleR=AnkleR
        self.LastFootR=FootR