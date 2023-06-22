from tools import norm, ang, angError, sat, speeds2motors, fixAngle, filt, L, unit, angl, norml, sats
from tools.interval import Interval
from control import Control
import numpy as np
import math
import time 

PLOT_CONTROL = False
if PLOT_CONTROL:
  import matplotlib.pyplot as plt

def close_event():
  plt.close() 


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
    self.plots = {"ref":[], "out": [], "eth":[], "vref": [], "v": [], "wref": [], "w": [], "sd": [], "injection": [], "dth": []}

  @property
  def error(self):
    return self.eth

  def abs_path_dth(self, initial_pose, error, field, step = 0.01, n = 10):
    pos = np.array(initial_pose[:2])
    thlist = np.array([])

    count = 0

    for i in range(n):
      th = field.F(pos)
      thlist = np.append(thlist, th)
      pos = pos + step * unit(th)
      count += 1

    aes = np.sum(np.abs(angError(thlist[1:], thlist[:-1]))) / n
  
    return aes + 0.05 * abs(error)

  def controlLine(self, x, xmax, xmin):
    return sats((xmax - x) / (xmax - xmin), 0, 1)


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

    # Tentativa de "remoção do controle de alto nível" do Luiz
    w = self.kp * eth + self.ki*self.integral

    # Velocidade limite de deslizamento
    v1 = self.amax / np.abs(w)

    # Velocidade limite das rodas
    v2 = self.vmax - self.L * np.abs(w) / 2

    # Velocidade limite de aproximação
    v3 = self.kp * norm(robot.pos, robot.field.Pb) ** 2 + robot.vref

    v  = min(v1, v2, v3)
    
    # Atualiza a última referência
    self.lastth = self.lastth[1:] + [th]
    robot.lastControlLinVel = v

    # Atualiza variáveis de estado
    self.eth = eth
    self.lastwref = w
    self.lastvref = v

    if PLOT_CONTROL:
      self.plots["eth"].append(eth * 180 / np.pi)
      self.plots["ref"].append(th * 180 / np.pi)
      self.plots["out"].append(robot.th * 180 / np.pi)
      self.plots["vref"].append(abs(v))
      self.plots["wref"].append(w)
      self.plots["v"].append(robot.velmod)
      self.plots["w"].append(robot.w)
      self.plots["sd"].append(sd)
      self.plots["injection"].append(injection)
      self.plots["dth"].append(dth)

      if len(self.plots["eth"]) >= 300 and robot.id == 0:
        t = np.linspace(0, 300 * 0.016, 300)
        fig = plt.figure()
        #timer = fig.canvas.new_timer(interval = 5000) 
        #timer.add_callback(close_event)
        plt.subplot(7,1,1)
        plt.plot(t, self.plots["eth"], label='eth')
        plt.plot(t, np.zeros_like(t), '--')
        plt.legend()
        plt.subplot(7,1,2)
        plt.plot(t, self.plots["ref"], '--', label='th_ref')
        plt.plot(t, self.plots["out"], label='th')
        plt.legend()
        plt.subplot(7,1,3)
        plt.plot(t, self.plots["vref"], '--', label='vref')
        plt.plot(t, self.plots["v"], label='v')
        plt.legend()
        plt.subplot(7,1,4)
        plt.plot(t, self.plots["wref"], '--', label='wref')
        plt.plot(t, self.plots["w"], label='w')
        plt.legend()
        plt.subplot(7,1,5)
        plt.plot(t, self.plots["sd"], label='sd')
        plt.legend()
        plt.subplot(7,1,6)
        plt.plot(t, self.plots["injection"], label='injection')
        plt.legend()
        plt.subplot(7,1,7)
        plt.plot(t, self.plots["dth"], label='dth')
        plt.legend()
        #timer.start()
        robot.stop()
        plt.show()
        #timer.stop()
        for plot in self.plots.keys(): self.plots[plot] = []
    
    #return (0,0)
    if robot.spin == 0: return (v * robot.direction, w)
    else: return (0, 60 * robot.spin)

