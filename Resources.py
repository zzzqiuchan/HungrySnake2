# -*- coding: utf-8 -*-

import pyglet

def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2
    
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

bread_image = pyglet.resource.image("bread.png")
brick_image = pyglet.resource.image("brick.png")

snakehead_image = pyglet.resource.image("snakehead.png")
snaketail_image = pyglet.resource.image("snaketail.png")
snakebody1_image = pyglet.resource.image("snakebody1.png")
snakebody2_image = pyglet.resource.image("snakebody2.png")

center_image(bread_image)
center_image(brick_image)
center_image(snakehead_image)
center_image(snakebody1_image)
center_image(snakebody2_image)
center_image(snaketail_image)

snakehead_rotation = {'right':0,'left':180,'up':-90,'down':90}
snaketail_rotation = {'right':0,'left':180,'up':-90,'down':90}
snakebody1_rotation = {'right':0,'left':0,'up':-90,'down':90}
snakebody2_rotation = {'upright':0, 'leftdown':0,
                        'rightdown':90,'upleft':90,
                        'rightup':180,'downleft':180,
                        'downright':-90,'leftup':-90}


background_image = pyglet.resource.image("background.png")