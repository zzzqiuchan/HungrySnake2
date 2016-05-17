# -*- coding: utf-8 -*-

import pyglet
import GameConfig
import Resources
from random import randint

class GameObject(pyglet.sprite.Sprite):
    def __init__(self, image, logicPoint, batch, group):
        self.logicPoint = logicPoint
        xx=GameConfig.basePoint[0]+logicPoint[0]*GameConfig.defaultImageWidth+GameConfig.defaultImageWidth/2#image.width
        yy=GameConfig.basePoint[1]+logicPoint[1]*GameConfig.defaultImageHeight+GameConfig.defaultImageHeight/2#image.height
        pyglet.sprite.Sprite.__init__(self, image, x=xx, y=yy, batch=batch, group=group)

    def getLogicPoint(self):
        return self.logicPoint
        
    def hit(self, logicPoint):
        return logicPoint == self.logicPoint
        
    def moveTo(self, logicPoint):
        self.logicPoint = logicPoint
        self.x=GameConfig.basePoint[0]+logicPoint[0]*GameConfig.defaultImageWidth+GameConfig.defaultImageWidth/2#image.width
        self.y=GameConfig.basePoint[1]+logicPoint[1]*GameConfig.defaultImageHeight+GameConfig.defaultImageHeight/2#image.height
        
class SnakeBody(GameObject):
    def __init__(self, logicPoint, batch, group, direction, type=0):
        self.direction = direction
        if 0 == type:#snake head
            GameObject.__init__(self, Resources.snakehead_image, logicPoint, batch, group)
            self.rotation = Resources.snakehead_rotation[direction]
        elif 1 == type:#snake body1
            GameObject.__init__(self, Resources.snakebody1_image, logicPoint, batch, group)
            self.rotation = Resources.snakebody1_rotation[direction]
        elif 2 == type:#snake tail
            GameObject.__init__(self, Resources.snaketail_image, logicPoint, batch, group)
            self.rotation = Resources.snaketail_rotation[direction]
    
    def changeToTail(self):
        self.image = Resources.snaketail_image
        self.rotation = Resources.snaketail_rotation[self.direction]
        
    def changeToBody(self, newDirection):
        if self.direction == newDirection:
            self.image = Resources.snakebody1_image
            self.rotation = Resources.snakebody1_rotation[self.direction]
        else:
            d = self.direction + newDirection
            self.direction = newDirection
            self.image = Resources.snakebody2_image
            self.rotation = Resources.snakebody2_rotation[d]
        
class Brick(GameObject):
    def __init__(self, logicPoint, batch, group):
        GameObject.__init__(self, Resources.brick_image, logicPoint, batch, group)

class Bread(GameObject):
    def __init__(self, logicPoint, batch, group):
        GameObject.__init__(self, Resources.bread_image, logicPoint, batch, group)
    
    def randomBread(self, snake, wall):
        count = 0
        while True:
            count += 1
            x = randint(0, GameConfig.maxX - 1)
            y = randint(0, GameConfig.maxY - 1)
            if snake.hitSnake((x, y)) or wall.hitWall((x,y)):
                if count > 200:
                    for x in range(0, GameConfig.maxX):
                        for y in range(0, GameConfig.maxY):
                            if snake.hitSnake((x, y)) or wall.hitWall((x,y)):
                                continue
                            else:
                                self.moveTo((x, y))
                                return True
                    self.moveTo((-1, -1))
                    return False
                else:
                    continue
            self.moveTo((x, y))
            return True