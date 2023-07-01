from tools import norm, ang, angError, sat, speeds2motors, fixAngle, filt, L, unit, angl, norml, sats
from tools.interval import Interval
from control import Control
import numpy as np
import math
import time 

class UFC_Simple(Control):
  """Controle unificado para o Univector Field, utiliza o ângulo definido pelo campo como referência \\(\\theta_d\\)."""
  def __init__(self, world, kw=4, kp=20, mu=0.3, vmax=1.5, L=L, enableInjection=False):
    Control.__init__(self, world)

    self.g = 9.8
    self.kw = kw
    self.kp = kp
    self.mu = mu
    self.amax = self.mu * self.g
    self.vmax = vmax
    self.L = L
    self.kv = 10
    self.ki = 10
    self.kd = 1
    self.integral = 0
    self.vbias = 0.2

    self.sd_min = 1e-4
    self.sd_max = 0.5

    self.lastth = [0,0,0,0]
    self.lastdth = 0
    self.interval = Interval(filter=False, initial_dt=0.016)
    self.lastnorm = 0
    self.enableInjection = enableInjection
    self.lastwref = 0
    self.lastvref = 0
    self.integrateinjection = 0
    self.loadedInjection = 0
    self.lastPb = np.array([0,0])
    self.vPb = np.array([0,0])

    self.eth = 0

  @property
  def error(self):
    return self.eth

  def output(self, robot):
    if robot.field is None: return 0,0
    # Ângulo de referência
    th = robot.field.F(robot.pose)

    # Erro angular
    eth = angError(th, robot.th)

    # Tempo desde a última atuação
    dt = self.interval.getInterval()

    # Calcula a integral e satura (descobrir o quanto saturar, tirei esse 64 rad/s)
    self.integral = sat(self.integral + eth * dt, 64)

    # Calcula a derivada
    # self.dth = eth/dt
    # print("dth: ", self.dth)

    # Velocidade angular com controle PID
    w = self.kp * eth + self.ki*self.integral# + self.kd*self.dth

    # Velocidade limite de deslizamento
    v1 = self.amax / np.abs(w)

    # Velocidade limite das rodas
    v2 = self.vmax - self.L * np.abs(w) / 2

    # Velocidade limite de aproximação
    v3 = self.kp * norm(robot.pos, robot.field.Pb) ** 2 + robot.vref

    v  = min(v1, v2, v3)
    if self.world.enableManualControl:
      v = self.world.manualControlSpeedV
      # w = self.world.manualControlSpeedW

    if robot.id == 0:
      print(f"ref(th): {(th * 180 / np.pi):.0f}º")
      print(f"erro(th): {(eth * 180 / np.pi):.0f}º")
      print(f"vref: {v:.2f}", end='')
      print(f", wref: {w:.2f}")
      print(f"v: {robot.velmod:.2f}", end='')
      print(f", w: {robot.w:.2f}")
    
    # Atualiza a última referência
    self.lastth = self.lastth[1:] + [th]
    robot.lastControlLinVel = v

    # Atualiza variáveis de estado
    self.eth = eth
    self.lastwref = w
    self.lastvref = v

    if robot.spin == 0: return (v * robot.direction, w)
    else: return (0, 60 * robot.spin)

