from client.referee import RefereeCommands, RefereePlacement
from client.gui import clientProvider
from strategy import MainStrategy
from UVF_screen import UVFScreen
from communication.serialRadio import SerialRadio
from world import World
from client import VSS

import matplotlib.pyplot as plt
import numpy as np
import logging
import time
import sys
from client.client_pickle import ClientPickle

class Loop:
    def __init__(
        self, 
        loop_freq=90, 
        draw_uvf=False, 
        team_yellow=True, 
        team_side=1, 
        immediate_start=False, 
        static_entities=False,
        port=5001,
        n_robots=3,
    ):
        # Instancia interface com o simulador
        #self.vss = VSS(team_yellow=team_yellow)

        # Instancia interfaces com o referee
        #self.rc = RefereeCommands()
        #self.rp = RefereePlacement(team_yellow=team_yellow)

        # Instancia o mundo e a estratégia
        self.world = World(n_robots=n_robots, side=team_side, team_yellow=team_yellow, immediate_start=immediate_start)
        self.strategy = MainStrategy(self.world, static_entities=static_entities)

        # Variáveis
        self.loopTime = 1.0 / loop_freq
        self.running = True
        self.lastupdatecount = 0
        self.pclient = ClientPickle(port)
        self.radio = SerialRadio()
        self.execute = False
        self.t0 = time.time()

        # Interface gráfica para mostrar campos
        self.draw_uvf = draw_uvf
        if self.draw_uvf:
            self.UVF_screen = UVFScreen(self.world, index_uvf_robot=1)
            self.UVF_screen.initialiazeScreen()
            self.UVF_screen.initialiazeObjects()
        
                   
        

    def loop(self):
        if self.world.updateCount == self.lastupdatecount: return
        
        print((time.time()-self.t0)*1000)
        self.t0 = time.time()
        
        self.lastupdatecount = self.world.updateCount

        # Executa estratégia
        self.strategy.update()

        # Executa o controle
        # control_output = [robot.entity.control.actuateNoControl(robot) for robot in self.world.team if robot.entity is not None]
        
        control_output = []
        for robot in self.world.team:
            # if robot.entity.__class__.__name__ == "GoalKeeper":
                # print('x_raw:', robot.x_raw, '. x:', self.world.field.side * robot.x_raw)
                # print('vx_raw:', robot.vx_raw, '. vx:', self.world.field.side * robot.vx_raw)
                # print('th_raw:', robot.th_raw, '. th:', self.world.field.side * robot.th_raw)
                # print('w_raw:', robot.w_raw, '. w:', self.world.field.side * robot.w_raw)

            if robot.entity is not None:
                if(robot.entity.__class__.__name__ == "GoalKeeper" or robot.entity.__class__.__name__ == "Defender"):
                    control_output.append(robot.entity.control.actuateNoControl(robot))
                else:
                    control_output.append(robot.entity.control.actuate(robot))

        # print('controle:', control_output)
        
        if self.execute:
            for robot in self.world.raw_team: robot.turnOn()   
            self.radio.send(control_output)
        else:
            self.radio.send([(0,0) for robot in self.world.team])
            for robot in self.world.raw_team: robot.turnOff()

        # Desenha no ALP-GUI
        self.draw()

    def busyLoop(self):
        message = self.pclient.receive()
        self.execute = message["running"]
        if message is not None: self.world.update(message)
        
        # command = self.rc.receive()
        # if command is not None: self.strategy.manageReferee(self.rp, command)

    def draw(self):
        for robot in [r for r in self.world.team if r.entity is not None]:
            clientProvider().drawRobot(robot.id, robot.x, robot.y, robot.thvec_raw.vec[0], robot.direction)

        # for robot in self.world.enemies:
        #     clientProvider().drawRobot(robot.id+3, robot.x, robot.y, robot.thvec_raw.vec[0], 1, (0.6, 0.6, 0.6))

        clientProvider().drawBall(0, self.world.ball.x, self.world.ball.y)

    def run(self):
        t0 = 0

        logging.info("System is running")
        
        while self.running:
            # Executa o loop de visão e referee até dar o tempo de executar o resto
            self.busyLoop()
            while time.time() - t0 < self.loopTime:
                self.busyLoop()
                
            # Tempo inicial do loop
            t0 = time.time()

            # Executa o loop
            self.loop()

            if self.draw_uvf:
                self.UVF_screen.updateScreen()

        logging.info("System stopped")