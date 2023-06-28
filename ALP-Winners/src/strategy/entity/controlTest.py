from ..entity import Entity
from strategy.field.UVF import UVF
from strategy.field.DirectionalField import DirectionalField
from strategy.field.goalKeeper import GoalKeeperField
from strategy.field.attractive import AttractiveField
from strategy.movements import goalkeep, spinGoalKeeper
from tools import angError, howFrontBall, howPerpBall, ang, norml, norm, angl, doSquareTest
from tools.interval import Interval
from control.goalKeeper import GoalKeeperControl
from control.UFC import UFC_Simple
import numpy as np
import math
import time

class ControlTester(Entity):
    def __init__(self, world, robot, side=1):
        super().__init__(world, robot)

        self._control = UFC_Simple(self.world)

    @property
    def control(self):
        return self._control

    def onExit(self):
        pass
        
    def directionDecider(self):
       if self.robot.field is not None:
            ref_th = self.robot.field.F(self.robot.pose)
            rob_th = self.robot.th

            if abs(angError(ref_th, rob_th)) > 90 * np.pi / 180:
                self.robot.direction *= -1
                self.lastChat = time.time()
            
            # Inverter a direção se o robô ficar preso em algo
            elif not self.robot.isAlive() and self.robot.spin == 0:
                if time.time()-self.lastChat > .3:
                    self.lastChat = time.time()
                    self.robot.direction *= -1

    def fieldDecider(self):
        Pb = doSquareTest(0,0,0,0)
        self.robot.field = UVF(Pb)
        self._control = UFC_Simple(self.world)

