# -*- coding: utf-8 -*-

import pyglet
from pyglet.window import key

from GameObject import SnakeBody
from GameObject import Bread

import GameConfig

moveX = {"up":0, "down":0, "left":-1, "right":1}
moveY = {"up":1, "down":-1, "left":0, "right":0}
directions = {"up":-1, "down":1, "left":2, "right":-2}

class Snake:
    def __init__(self, theBatch, theGroup):
        self.batch = theBatch
        self.group = theGroup
        
        self.body = []
        self.logicBody = []
        self.headPoint = (-1,-1)
        self.direction = ''
        self.change_direction = ''
        self.speed = 0.25
        self.count = 0.0
        
        self.msg_label = pyglet.text.Label(text="Length:", 
            x=GameConfig.msg2_x, y=GameConfig.msg2_y,
            batch=theBatch, group=theGroup,
            color=GameConfig.textColor, font_size=GameConfig.textSize)
    
    def newSnake(self, logicPoint, direction):
        self.logicBody = []
        for b in self.body:
            b.delete()
        self.body = []
        
        self.headPoint = logicPoint
        self.direction = direction
        
        #head
        self.logicBody.insert(0, logicPoint)
        self.body.insert(0, SnakeBody(logicPoint, self.batch, self.group, direction, 0))
        #body
        newPoint = (logicPoint[0] - moveX[direction], logicPoint[1] - moveY[direction])
        self.logicBody.insert(0, newPoint)
        self.body.insert(0, SnakeBody(newPoint, self.batch, self.group, direction, 1))
        #body
        newPoint = (newPoint[0] - moveX[direction], newPoint[1] - moveY[direction])
        self.logicBody.insert(0, newPoint)
        self.body.insert(0, SnakeBody(newPoint, self.batch, self.group, direction, 1))
        #tail
        newPoint = (newPoint[0] - moveX[direction], newPoint[1] - moveY[direction])
        self.logicBody.insert(0, newPoint)
        self.body.insert(0, SnakeBody(newPoint, self.batch, self.group, direction, 2))
        
        self.msg_label.text = 'Length:' + str(len(self.logicBody))
        
    def hitSnake(self, logicPoint):
        if logicPoint in self.logicBody:
            return True
        else:
            return False
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.change_direction = 'left'
        if symbol == key.RIGHT:
            self.change_direction = 'right'
        if symbol == key.UP:
            self.change_direction = 'up'
        if symbol == key.DOWN:
            self.change_direction = 'down'
            
    def update(self, dt, wall, bread):
        self.count += dt
        key_pressed = False
        new_direction = ''

        if self.change_direction != '':
            dd = directions[self.change_direction] + directions[self.direction]
            if dd != 0:#有效按键
                new_direction = self.change_direction
            self.change_direction = ''
        
        if new_direction == '':
            if self.count >= self.speed:
                new_direction = self.direction
            else:
                return 1
        
        newPoint = self.headPoint
        newPoint = (newPoint[0] + moveX[new_direction], newPoint[1] + moveY[new_direction])
        
        if newPoint[0] >= GameConfig.maxX:
            newPoint = (0, newPoint[1])
        elif newPoint[0] < 0:
            newPoint = (GameConfig.maxX - 1, newPoint[1])
        if newPoint[1] >= GameConfig.maxY:
            newPoint = (newPoint[0], 0)
        elif newPoint[1] < 0:
            newPoint = (newPoint[0], GameConfig.maxY - 1)
        
        if newPoint in self.logicBody:
            if newPoint != self.logicBody[0]:#旧的尾部可以碰
                return -1
        if wall.hitWall(newPoint):
            return -2
        
        self.count = 0
        self.direction = new_direction
        #更新头部
        self.headPoint = newPoint
        self.body[-1].changeToBody(new_direction)
        self.logicBody.append(newPoint)
        self.body.append(SnakeBody(newPoint, self.batch, self.group, new_direction, 0))
        
        if bread.hit(newPoint):#吃到食物，不更新尾巴
            self.msg_label.text = 'Length:' + str(len(self.logicBody))
            if bread.randomBread(self, wall):
                return 1
            else:
                return -3
        #更新尾巴
        self.logicBody.pop(0)
        self.body.pop(0).delete()
        self.body[0].changeToTail()
        
        return 1