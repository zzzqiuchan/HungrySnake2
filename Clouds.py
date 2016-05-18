# -*- coding: utf-8 -*-

import pyglet

import random
import Resources, GameConfig

class Cloud(pyglet.sprite.Sprite):
    def __init__(self, image, y, batch, group):
        s = random.random() / 4.0 + 0.25
        self.half_width = image.width*0.5*s
        x = GameConfig.windowWidth + self.half_width
        
        pyglet.sprite.Sprite.__init__(self, image, x=x, y=y, batch=batch, group=group)
        self.scale = s
        self.speed = 20 + random.randint(0, 40)
        self.dead = False
        
    def update(self, dt):
        self.x = self.x - dt * self.speed
        if self.x + self.half_width <= 0:
            self.dead = True
    
class Clouds:
    def __init__(self, batch, group):
        self.batch = batch
        self.group = group
        self.clouds = []
        
    def newCloud(self):
        y = random.randint(0, GameConfig.windowHeight - 8)
        if random.random() > 0.4:
            self.clouds.append(Cloud(Resources.cloud1_image, y, self.batch, self.group))
        else:
            self.clouds.append(Cloud(Resources.cloud2_image, y, self.batch, self.group))
        
    def update(self, dt):
        for c in self.clouds:
            c.update(dt)
            if c.dead:
                c.delete()
                self.clouds.remove(c)
        
        if len(self.clouds) < 3:
            if random.randint(1, 500) < 3:
                self.newCloud()
        