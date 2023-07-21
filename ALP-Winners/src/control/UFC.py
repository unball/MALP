from tools import norm, ang, angError, sat, speeds2motors, fixAngle, filt, L, unit, angl, norml, sats
from tools.interval import Interval
from control import Control
import numpy as np
import math
import time 

class UFC_Simple(Control):
  """Controle unificado para o Univector Field, utiliza o ângulo definido pelo campo como referência \\(\\theta_d\\)."""
  def __init__(self, world, kw=4, kp=20, mu=0.3, vmax=1.0, L=L, enableInjection=False):
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


    self.lastth = 0
    self.interval = Interval(filter=False, initial_dt=0.016)

  def output(self, robot):
    if robot.field is None: return 0,0
    # Ângulo de referência
    th = robot.field.F(robot.pose)

    # Erro angular
    eth = angError(th, robot.th)

    # Tempo desde a última atuação
    dt = self.interval.getInterval()

    # Derivada da referência
    dth = sat(angError(th, self.lastth) / dt, 15)

    # Computa phi
    phi = robot.field.phi(robot.pose)

    # Computa gamma
    gamma = robot.field.gamma(dth, robot.velmod, phi)

    # Computa omega
    omega = self.kw * np.sign(eth) * np.sqrt(np.abs(eth)) + gamma

    # Velocidade limite de deslizamento
    if phi != 0: v1 = (-np.abs(omega) + np.sqrt(omega**2 + 4 * np.abs(phi) * self.amax)) / (2*np.abs(phi))
    if phi == 0: v1 = self.amax / np.abs(omega)

    # Velocidade limite das rodas
    v2 = (2*self.vmax - self.L * np.abs(omega)) / (2 + self.L * np.abs(phi))

    # Velocidade limite de aproximação
    v3 = self.kp * norm(robot.pos, robot.field.Pb) ** 2 + robot.vref

    # Velocidade linear é menor de todas
    v  = max(min(v1, v2, v3), 0)

    # Lei de controle da velocidade angular
    w = v * phi + omega

    if robot.id == 0:
      print(f"ref(th): {(th * 180 / np.pi):.0f}º")
      print(f"erro(th): {(eth * 180 / np.pi):.0f}º")
      print(f"vref: {v:.2f}", end='')
      print(f", wref: {w:.2f}")
      print(f"v: {robot.velmod:.2f}", end='')
      print(f", w: {robot.w:.2f}")
    
    # Atualiza a última referência
    self.lastth = th
    robot.lastControlLinVel = v

    if robot.spin == 0: return (v * robot.direction, w)
    else: return (0, 60 * robot.spin)