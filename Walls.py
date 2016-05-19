# -*- coding: utf-8 -*-

from GameObject import Brick
import GameConfig

class Walls:
    def __init__(self, batch, group):
        self.logicBricks = []
        self.bricks = []
        self.batch = batch
        self.group = group
                    
    def newWalls(self, logicMap):
        self.logicBricks = []
        for b in self.bricks:
            b.delete()
        self.bricks = []
        
        for _x in range(0, GameConfig.maxX):
            for _y in range(0, GameConfig.maxY):
                if logicMap[_y][_x] == 1:
                    x = _x
                    y = GameConfig.maxY - _y - 1
                    newPoint = (x, y)
                    self.logicBricks.append(newPoint)
                    newBrick = Brick(newPoint, self.batch, self.group)
                    self.bricks.append(newBrick)
        
    def hitWall(self, logicPoint):
        if logicPoint in self.logicBricks:
            return True
        else:
            return False