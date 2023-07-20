from abc import ABC, abstractmethod
from tools import speeds2motors, deadzone, sat
from control.motorControl import MotorControl
import numpy as np
import time


class Control(ABC):
    def __init__(self, world):
        ABC.__init__(self)

        self.world = world
        self.motor_vr_control = MotorControl(3, 0.2 , 0.05, 32)
        self.motor_vl_control = MotorControl(3, 0.2, 0.05, 32)
        # self.motor_vr_control = MotorControl(1, 1, 3, 32)
        # self.motor_vl_control = MotorControl(1, 1, 3, 32)

        self.last_w = 0

    @abstractmethod
    def output(self, robot):
        pass

    def actuateNoControl(self, robot):
        if not robot.on:
            return (0, 0)

        v, w = self.output(robot)
        # v = 0.1 * np.sign(np.sin(2*np.pi*0.5*time.time()))
        # w = 0
        robot.lastControlLinVel = v
        
        vr, vl = speeds2motors(v, w)
        
        vr = 3*int(sat(vr * 127 / 110, 127))
        vl = 3*int(sat(vl * 127 / 110, 127))
        
        return vr, vl

    def actuate(self, robot):
        if not robot.on:
            return (0, 0)


