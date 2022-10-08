from abc import ABC, abstractmethod
import time
import numpy as np
from controller.vision.server_pickle import ServerPickle
from controller.vision.cameras import CameraHandler
from controller.vision.visionMessage import VisionMessage

class Vision(ABC):
  """Classe que define as interfaces que qualquer sistema de visão deve ter no sistema."""
  
  def __init__(self, world, port):
    super().__init__()
    
    self.cameraHandler = CameraHandler()
    """Instancia módulo `MainSystem.controller.vision.cameras.CameraHandler` que gerencia as câmeras e retorna os frames"""
    
    self._world = world
    """Mantém referência ao mundo"""

    self.usePastPositions = False
    self.lastCandidateUse = 0
  
    self.server_pickle = ServerPickle(port)

  @abstractmethod
  def process(self, frame):
    """Método abstrato que recebe um frame do tipo numpy array no formato (height, width, depth). Retorna uma mensagem de alteração do tipo `MainSystem.controller.vision.visionMessage.VisionMessage`"""
    pass
    
  def giveUpAndWait(self):
    """Método que impõe um atraso de 30ms por falta de frame."""
    time.sleep(0.03)
    return False
  
  def update(self):
    """Obtém um frame da câmera, chama o `Vision.process` e atualiza o mundo (`World`) com base na mensagem retornada. Retorna `False` se nada foi feito e `True` se atualizou o mundo."""
    
    frame = self.cameraHandler.getFrame()
    if frame is None: return self.giveUpAndWait()
    
    # Renova a identificação a cada 2 segundos
    if time.time()-self.lastCandidateUse > 0.66 and np.all([x.spin == 0 for x in self._world.robots]):
      self.usePastPositions = False
   
    data = self.process(frame)
    self._world.update(data)
    message = {
      'Ball':{
        'x': self._world.ball.pos[0],
        'y': self._world.ball.pos[1],
        'vx': self._world.ball.vel[0],
        'vy': self._world.ball.vel[1]
      },
      'Robots': [
        {
          'x': self._world.robots[i].pose[0],
          'y': self._world.robots[i].pose[1],
          'orientation': self._world.robots[i].pose[2],
          'vx': self._world.robots[i].vel[0],
          'vy': self._world.robots[i].vel[1],
          'vangular': self._world.robots[i].w
        }
        for i in range(self._world.n_robots)
      ]
    }
    # print('-'*20)
    # print('Robots:')
    # for robot in message['Robots']:
    #   print(type(robot), robot)

    self.server_pickle.send(message)

    if self.usePastPositions is False:
      self.usePastPositions = True
      self.lastCandidateUse = time.time()
    
    return True
