from .elements import *

class Field:
    def __init__(self, side):
        self.width = 1.75
        self.height = 1.35
        self.goalAreaWidth = 0.15
        self.goalAreaHeight = 0.70

        self.xmargin = 0.30
        self.ymargin = 0.18
        self.side = side

        self.areaEllipseSize = (0.35, 0.52)
        self.areaEllipseCenter = (-self.maxX + 0.10, 0)

    @property
    def maxX(self):
        return self.width / 2

    @property
    def maxY(self):
        return self.height / 2

    @property
    def size(self):
        return (self.maxX, self.maxY)

    @property
    def marginX(self):
        return self.maxX - self.xmargin
    
    @property
    def marginY(self):
        return self.maxY - self.ymargin

    @property
    def marginPos(self):
        return (self.marginX, self.marginY)

    @property
    def goalPos(self):
        return (self.maxX, 0)

    @property
    def goalAreaSize(self):
        return (self.goalAreaWidth, self.goalAreaHeight)

class World:
    def __init__(self, n_robots=5, side=1, vss=None, team_yellow=False, immediate_start=False):
        self.n_robots = n_robots
        self._team = [TeamRobot(self, i, on=immediate_start) for i in range(self.n_robots)]
        self.enemies = [TeamRobot(self, i, on=immediate_start) for i in range(self.n_robots)]
        self.ball = Ball(self)
        self.field = Field(side)
        self.vss = vss
        self.team_yellow = team_yellow
        self.allyGoals = 0
        self.enemyGoals = 0
        self.updateCount = 0
        self.checkBatteries = False
        self.manualControlSpeedV = 0
        self.manualControlSpeedW = 0
        
    def update(self, message):
        if self.team_yellow: 
            yellow = self.team
            blue = self.enemies
        else:
            yellow = self.enemies
            blue = self.team

        robot_id = 0
        for robot in range(message["n_robots"]):
            if self.team_yellow: 
                yellow[robot_id].update(
                    message["robots"][robot_id]["pos_x"], 
                    message["robots"][robot_id]["pos_y"], 
                    message["robots"][robot_id]["th"], 
                    message["robots"][robot_id]["vel_x"], 
                    message["robots"][robot_id]["vel_y"], 
                    message["robots"][robot_id]["w"]
                )
            else:
                blue[robot_id].update(
                    message["robots"][robot_id]["pos_x"], 
                    message["robots"][robot_id]["pos_y"], 
                    message["robots"][robot_id]["th"], 
                    message["robots"][robot_id]["vel_x"], 
                    message["robots"][robot_id]["vel_y"], 
                    message["robots"][robot_id]["w"]
                )
            robot_id+=1
       
        self.ball.update(message["ball"]["pos_x"], message["ball"]["pos_y"], message["ball"]["vel_x"], message["ball"]["vel_y"])
        self.checkBatteries = message["check_batteries"]
        self.manualControlSpeedV = message["manualControlSpeedV"]
        self.manualControlSpeedW = message["manualControlSpeedW"]

        self.updateCount += 1

    def addAllyGoal(self):
        print("Gol aliado!")
        self.allyGoals += 1

    def addEnemyGoal(self):
        print("Gol inimigo!")
        self.enemyGoals += 1

    @property
    def goals(self):
        return self.allyGoals + self.enemyGoals

    @property
    def balance(self):
        return self.allyGoals - self.enemyGoals

    @property
    def team(self):
        return self._team#[robot for robot in self._team if robot.on]

    @property
    def raw_team(self):
        return self._team