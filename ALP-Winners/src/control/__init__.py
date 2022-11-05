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

    def get_references(self, robot):
        return robot.v_signed, self.last_w + sat(robot.angvel-self.last_w, 0.1)

    def actuate(self, robot):
        """Malha acoplada, controle para v e w"""
        
        v_ref, w_ref = self.get_references(robot)
        v, w = self.output(robot)


        e_ang = k_lin * (w_ref - w)
        e_lin = k_ang * (v_ref - v)

        e_left = e_lin - e_ang
        e_right = e_lin + e_ang

        # verificar sinais no matlab
        return (self.motor_vr_control.actuate(e_right),
                self.motor_vl_control.actuate(e_left))

    def actuate_theta(self, robot):
        """Controle para v e theta"""

        v_ref, w_ref = self.get_references(robot)
        v, w = self.output(robot)


        # e_lin = k_ang * (v_ref - v)
        e_ang = (theta_ref - theta) * (s + a) # domínio de laplace, ou seja, derivada do erro angular (theta_ref - theta) 
        e_ang = k_lin * (w_ref - w)

        e_left = e_lin - e_ang
        e_right = e_lin + e_ang

        # Identificaçao do motor (não tem que ser precisa):
        #   Obter constante de tempo para chutar o zero

        # verificar sinais corretos no matlab
        return (self.motor_vr_control.actuate(e_right),
                self.motor_vl_control.actuate(e_left))


    def actuate(self, robot):
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
            pass
            # print(
            #     f"ur: {ur}\ter: {vr - vision_vr}, vr: {vr}, vision_vr: {vision_vr}")
            # print(
            #     f"ul: {ul}\tel: {vl - vision_vl}, vl: {vl}, vision_vl: {vision_vl}")
            # print(
            #     f"ur: {ur}\tev: {v - robot.v_signed}, v: {v}, vision_v: {robot.v_signed}")
            # print(
            #     f"ul: {ul}\tew: {w - vision_w}, w: {w}, vision_w: {vision_w}")

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
