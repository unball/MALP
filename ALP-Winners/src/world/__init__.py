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

        self.areaEllipseSize = (0.35, 0.50)
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
        self._team = [TeamRobot(self, i, on=immediate_start) for i in range(n_robots)]
        self.enemies = [TeamRobot(self, i, on=immediate_start) for i in range(n_robots)]
        self.ball = Ball(self)
        self.field = Field(side)
        self.vss = vss
        self.team_yellow = team_yellow

        self.allyGoals = 0
        self.enemyGoals = 0
        self.updateCount = 0

    def update(self, message):
        # teamPos = zip(message["ally_x"], message["ally_y"], message["ally_th"], message["ally_vx"], message["ally_vy"], message["ally_w"])
        # enemiesPos = zip(message["enemy_x"], message["enemy_y"], message["enemy_th"], message["enemy_vx"], message["enemy_vy"], message["enemy_w"])

        if self.team_yellow: 
            yellow = self.team
            blue = self.enemies
        else:
            yellow = self.enemies
            blue = self.team

        robot_id = 0
        for robot in range(message[4]):
            if self.team_yellow: 
                yellow[robot_id].update(message[5+6*robot], message[6+6*robot], message[7+6*robot], message[8+6*robot], message[9+6*robot], message[10+6*robot])
            else:
                blue[robot_id].update(message[5+6*robot], message[6+6*robot], message[7+6*robot], message[8+6*robot], message[9+6*robot], message[10+6*robot])
            robot_id+=1
        # for robot, pos in zip(self.team, teamPos): robot.update(*pos)
        # for robot, pos in zip(self.enemies, enemiesPos): robot.update(*pos)
        #self.ball.update(message["ball_x"], message["ball_y"], message["ball_vx"], message["ball_vy"])
        self.ball.update(message[0], message[1], message[2], message[3])
        # print(f'\nBall: x = {self.ball.pos[0]}, y = {self.ball.pos[1]}, vx = {self.ball.v[0]}, vy = {self.ball.v[1]}')

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