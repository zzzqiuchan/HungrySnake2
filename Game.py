# -*- coding: utf-8 -*-

import pyglet

import GameObject
from Walls import Walls
from Snake import Snake
from Clouds import Clouds
import Resources, GameConfig

game_window = pyglet.window.Window(width=GameConfig.windowWidth,
    height=GameConfig.windowHeight, caption=GameConfig.windowCaption)

main_batch = pyglet.graphics.Batch()
background_group = pyglet.graphics.OrderedGroup(0)
middleground_group = pyglet.graphics.OrderedGroup(1)
foreground_group = pyglet.graphics.OrderedGroup(2)

class Game:
    def __init__(self, gameWindow, mainBatch, backgroundGroup, middlegroundGroup, foregroundGroup):
        self.mainBatch = mainBatch
        self.backgroundGroup = backgroundGroup
        self.middlegroundGroup = middlegroundGroup
        self.foregroundGroup = foregroundGroup
        #背景图与方框
        self.background = pyglet.sprite.Sprite(img=Resources.background_image,x=0,y=0,batch=mainBatch,group=backgroundGroup)
        x1 = GameConfig.basePoint[0]
        y1 = GameConfig.basePoint[1]
        ww = GameConfig.maxX * GameConfig.defaultImageWidth
        hh = GameConfig.maxY * GameConfig.defaultImageHeight
        self.rect_vertex_list = mainBatch.add(4, pyglet.gl.GL_LINE_LOOP, middlegroundGroup,
            ('v2f', (x1,y1,x1+ww,y1,x1+ww,y1+hh,x1,y1+hh)), ('c3B', GameConfig.rectColor*4))
        #整体文本信息
        self.msg_label = pyglet.text.Label(text="Welcome!", 
            x=GameConfig.msg1_x, y=GameConfig.msg1_y,
            batch=mainBatch, group=middlegroundGroup,
            color=GameConfig.textColor, font_size=GameConfig.textSize)
        #初始食物
        self.bread = GameObject.Bread(GameConfig.firstFood, self.mainBatch, middlegroundGroup)
        #障碍物们
        self.walls = Walls(mainBatch, middlegroundGroup)
        self.walls.newWalls(GameConfig.logicMap)
        #蛇
        self.snake = Snake(mainBatch,middlegroundGroup)
        self.snake.newSnake(GameConfig.startPoint, GameConfig.startDirection)
        gameWindow.push_handlers(self.snake)
        #飘过的云
        self.clouds = Clouds(mainBatch, foregroundGroup)
    
    def update(self, dt):
        self.snake.update(dt, self.walls, self.bread)
        self.clouds.update(dt)

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

if __name__ == "__main__":
    game=Game(game_window, main_batch, background_group, middleground_group, foreground_group)

    pyglet.clock.schedule_interval(game.update, 1/120.0)

    pyglet.app.run()