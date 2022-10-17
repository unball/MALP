from abc import ABC, abstractmethod
from tools import speeds2motors, deadzone, sat
from control.motorControl import MotorControl
import numpy as np
import time


class Control(ABC):
    def __init__(self, world):
        ABC.__init__(self)

        self.world = world
        self.motor_vr_control = MotorControl(4, 0.18, 0.1, 30)
        self.motor_vl_control = MotorControl(4, 0.18, 0.1, 30)

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
        return (100,100)
        if not robot.on:
            return (0, 0)

        v, w = self.output(robot)
        # v = 0.1 * np.sign(np.sin(2*np.pi*0.5*time.time()))
        # w = 0
        robot.lastControlLinVel = v
        
        vr, vl = speeds2motors(v, w)
        vision_w = self.last_w + sat(robot.angvel-self.last_w, 0.1)
        vision_vr, vision_vl = speeds2motors(robot.v_signed, vision_w)

        ur = self.motor_vr_control.actuate(vr, vr - vision_vr)
        ul = self.motor_vl_control.actuate(vl, vl - vision_vl)

        if robot.id == 0:
            # print(
            #     f"ur: {ur}\ter: {vr - vision_vr}, vr: {vr}, vision_vr: {vision_vr}")
            # print(
            #     f"ul: {ul}\tel: {vl - vision_vl}, vl: {vl}, vision_vl: {vision_vl}")
            print(
                f"ur: {ur}\tev: {v - robot.v_signed}, v: {v}, vision_v: {robot.v_signed}")
            print(
                f"ul: {ul}\tew: {w - vision_w}, w: {w}, vision_w: {vision_w}")

        # vr, vl = speeds2motors(uv, uw)

        self.last_w = vision_w
        return ur, ul

        # vr, vl = speeds2motors(v, self.world.field.side * w)

        # # return (vr, vl)

        # vision_vr, vision_vl = speeds2motors(robot.velmod, robot.angvel)

        # ur = self.motor_r_control.actuate(vr - vision_vr)
        # ul = self.motor_l_control.actuate(vl - vision_vl)

        # if robot.id == 0:
        #     print(f"ur: {ur}, e: {vr-vision_vr}, vr: {vr}, vision_vr: {vision_vr}")

        # return (int(ur), int(ul))
