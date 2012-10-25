# -*- coding: utf-8 -*-
##############################################################
##
##############################################################

import jngl
from GameObject import GameObject
import random
import copy
from math import sin
SOUND = "sound/"

RESOURCEWORLD = "img/World/"
class Spike(GameObject):
    img = RESOURCEWORLD + "spike.png"
    width = jngl.getWidth(img)
    height = jngl.getHeight(img)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def drawPreview(self):
        jngl.setSpriteColor(255, 255, 255, 100)
        self.draw()
        jngl.setSpriteColor(255, 255, 255)
    def draw(self):
        jngl.draw(self.img,self.x, self.y)
    def handleCollision(self, player):
        player.kill()

class Key(GameObject):
    img = RESOURCEWORLD + "key.png"
    width = jngl.getWidth(img)
    height = jngl.getHeight(img)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def drawPreview(self):
        jngl.setSpriteColor(255, 255, 255, 100)
        self.draw()
        jngl.setSpriteColor(255, 255, 255)
    def draw(self):
        jngl.draw(self.img,self.x, self.y)
    def step(self):
        pass
    def handleCollision(self, player):
        self.game.level.objects.remove(self)
        player.hasKey = True

class Lock(GameObject):
    img = RESOURCEWORLD + "lock.png"
    width = jngl.getWidth(img)
    height = jngl.getHeight(img)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def drawPreview(self):
        jngl.setSpriteColor(255, 255, 255, 100)
        self.draw()
        jngl.setSpriteColor(255, 255, 255)
    def isBox(self):
        return True
    def draw(self):
        jngl.draw(self.img,self.x, self.y)
    def handleCollision(self, player):
        #if self in self.game.level.objects and player.hasKey:
        #    self.game.level.objects.remove(self)
        if player.hasKey:
            self.game.level.objects.remove(self)

class NoJumpArea(GameObject):
    img = RESOURCEWORLD + "yellow_black.png"
    width = jngl.getWidth(img)
    height = jngl.getHeight(img)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def drawPreview(self):
        jngl.setSpriteColor(255, 255, 255, 100)
        self.draw()
        jngl.setSpriteColor(255, 255, 255)
    def draw(self):
        jngl.draw(self.img, self.x, self.y)
    def handleCollision(self, player):
        player.canJump = False

class SlowArea(GameObject):
    img = RESOURCEWORLD + "slow.png"
    width = jngl.getWidth(img)
    height = jngl.getHeight(img)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def drawPreview(self):
        jngl.setSpriteColor(255, 255, 255, 100)
        self.draw()
        jngl.setSpriteColor(255, 255, 255)
    def draw(self):
        jngl.draw(self.img, self.x, self.y)
    def handleCollision(self, player):
        player.xspeed *= 0.8

class Box(GameObject):
    textureSize = 32
    texture = RESOURCEWORLD + "boxtex.png"
    gras_texture = RESOURCEWORLD + "gras.png"
    def __init__(self, x, y, width = 32, height = 32):
        self.x = x
        self.y = y
        self.xspeed = 0
        self.yspeed = 0
        self.width = width
        self.height = height
        if self.width < 0:
            self.width = -self.width
            self.x -= self.width
        if self.height < 0:
            self.height = -self.height
            self.y -= self.height
    def isBox(self):
        return True
    def drawPreview(self):
        self.draw()
    def draw(self):
        #jngl.setColor(200, 200, 200)
        #jngl.drawRect(self.x, self.y, self.width, self.height)
        for x in range(0, self.width, self.textureSize):
            for y in range(0, self.height, self.textureSize):
                jngl.draw(self.texture, self.x + x, self.y + y)
                if y == 0:
                    jngl.draw(self.gras_texture, self.x + x, self.y)

class PassableBox(Box):
    def __init__(self, x, y, width = 32, height = 32):
        Box.__init__(self,x,y,width,height)
    def checkCollision(self, other):
        return False
    def drawPreview(self):
        jngl.setSpriteColor(100,100,255,50)
        self.draw()
        jngl.setSpriteColor(255,255,255)    
class MovingBox(Box):
    textureSize = 32
    texture = RESOURCEWORLD + "movingbox.png"
    gras_texture = RESOURCEWORLD + "gras.png"
    def __init__(self, x, y, width = 32, height = 32, movetoX = 100, movetoY = 100):
        Box.__init__(self,x,y,width,height)
        self.countdown = 0
        self.moveLeft = True
        if movetoX < 0:
            self.moveLeft = False
        self.movetoX = movetoX
    def step(self):
        if self.countdown == 0:
            self.countdown = abs(self.movetoX)
            self.moveLeft = not self.moveLeft
        if self.moveLeft:
            self.x -= 1
        else:
            self.x += 1
        self.countdown -= 1
    def handleCollision(self, player):
        if self.moveLeft:
                player.x -=1
                player.error_correction_x -=1.1
        else:
            player.x +=1
            player.error_correction_x +=1.1
 
class FragileBox(Box):
    texture2 = RESOURCEWORLD + "fragileboxtex.png"
    texture3 = RESOURCEWORLD + "fragileboxtex2.png"
    def __init__(self, x, y, width = 32, height = 32, health = 1000, stability = 5):
        Box.__init__(self,x,y,width,height)
        self.health = health
        self.stability = stability
        self.colliding = 0
    
    def handleCollision(self, player):
        Box.handleCollision(self,player)
        self.colliding += 1
    
    def step(self):
        if self.colliding > self.stability:
            self.health -= 1
            if self.health < 1:
                self.game.level.objects.remove(self)
        self.colliding = 0
    
    def drawPreview(self):
        v = self.health
        self.health = 1
        self.draw()
        self.health = v
        
    def draw(self):
        #jngl.setColor(200, 200, 200)
        #jngl.drawRect(self.x, self.y, self.width, self.height)
        tex = self.texture
        if self.health < 500:
            tex = self.texture2
            if self.health < 250:
                tex = self.texture3
        for x in range(0, self.width, self.textureSize):
            for y in range(0, self.height, self.textureSize):
                jngl.draw(tex, self.x + x, self.y + y)
                if y == 0:
                    jngl.draw(self.gras_texture, self.x + x, self.y)
        

class InvisibleBox(Box):
    def __init__(self, x, y, width = 32, height = 32):
        Box.__init__(self,x,y,width,height)
        self.opacity = 100
    def step(self):
        Box.step(self)
        if self.opacity > 0:
            self.opacity -=1
    def handleCollision(self, player):
        Box.handleCollision(self,player)
        if self.opacity < 254:
            self.opacity += 2
             
    def drawPreview(self):
        self.draw(100)
        
    def draw(self, opacity = 0):
        jngl.setSpriteColor(255, 255, 255, self.opacity)
        if opacity >0:
            jngl.setSpriteColor(255, 255, 255, opacity)
        #jngl.drawRect(self.x, self.y, self.width, self.height)
        for x in range(0, self.width, self.textureSize):
            for y in range(0, self.height, self.textureSize):
                jngl.draw(self.texture, self.x + x, self.y + y)
                if y == 0:
                    jngl.draw(self.gras_texture, self.x + x, self.y)
        jngl.setSpriteColor(255,255,255)

class PulsatingBox(Box):
    def __init__(self, x, y, width = 32, height = 32):
        Box.__init__(self,x,y,width,height)
        self.opacity = 255
        self.show = True
        
    def step(self):
        Box.step(self)
        
        if self.opacity < 1 or self.opacity > 254:
            self.show = not self.show
        if self.show:
            self.opacity +=1
        else:
            self.opacity -=1
            
    def checkCollision(self, other):
        if self.opacity > 20:
            return GameObject.checkCollision(self, other)
        else: return False
                 
    def drawPreview(self):
        self.draw(50)
        
    def draw(self, opacity = 0):
        jngl.setSpriteColor(255, 255, 255, self.opacity)
        if opacity >0:
            jngl.setSpriteColor(255, 255, 255, opacity)
        #jngl.drawRect(self.x, self.y, self.width, self.height)
        for x in range(0, self.width, self.textureSize):
            for y in range(0, self.height, self.textureSize):
                jngl.draw(self.texture, self.x + x, self.y + y)
                if y == 0:
                    jngl.draw(self.gras_texture, self.x + x, self.y)
        jngl.setSpriteColor(255,255,255)

class Goal(GameObject):
    img = RESOURCEWORLD + "goal.png"
    width = jngl.getWidth(img)
    height = jngl.getHeight(img)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def drawPreview(self):
        jngl.setSpriteColor(255, 255, 255, 100)
        self.draw()
        jngl.setSpriteColor(255, 255, 255)
    def draw(self):
        jngl.draw(self.img,self.x, self.y)
    def step(self):
        pass
    def handleCollision(self, player):
        player.goal()


class Spawner(GameObject):
    img = RESOURCEWORLD + "spawner_2.png"
    width = jngl.getWidth(img)
    height = jngl.getHeight(img)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spawns = True
        self.quantity = 10

    def drawPreview(self):
        jngl.setSpriteColor(255, 255, 255, 100)
        self.draw()
        jngl.setSpriteColor(255, 255, 255)
    def draw(self):
        jngl.draw(self.img,self.x, self.y)
    def handleCollision(self, player):
        if self.spawns:
            self.spawns = False
            player.game.level.objects.remove(self)
        while self.quantity:
            p = copy.copy(player)
            #p.x += random.randint(-10,10)
            p.hasKey = False
            p.xspeed += random.randint(-50,50)/10.0
            p.yspeed = -random.randint(0,100)/10.0
            self.quantity-=1
            self.game.level.somyeols.append(p)

class Firetrap(GameObject):
    img = RESOURCEWORLD + "fire.png"
    fire = (RESOURCEWORLD+"flame0.png", RESOURCEWORLD+"flame1.png",
            RESOURCEWORLD+"flame2.png", RESOURCEWORLD+"flame3.png")
    width = jngl.getWidth(img)
    height = 96
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = False
        self.countdown = 0
        self.animation = 0
        self.anim_size = 0
##        self.particles = []
    
    def initGame(self, game):
        GameObject.initGame(self, game)
        self.active = False
        self.countdown = 0
        self.animation = random.randint(0,300)*.01
        self.anim_size = 0
        
    def step(self):
        self.countdown += 1
        if self.countdown > 150:
            self.countdown = 0
            self.active = not self.active
        self.animation += .08
        self.animation %= 4
        if self.countdown < 30:
            self.anim_size += .3
        elif self.countdown > 120:
            self.anim_size -= .3

    def drawPreview(self):
        jngl.draw(self.img, self.x, self.y + self.height)
        jngl.drawScaled(self.fire[0], self.x, self.y, 1, 1.8)
    def drawEditor(self):
        self.drawPreview()
    def draw(self):
        jngl.draw(self.img, self.x, self.y + self.height)
        if self.active:
            xs = (self.anim_size*.13)-(.1*sin(self.animation))
            ys = self.anim_size*.2+(.1*sin(self.animation))
            y = self.y + (114-(64 * ys))
            x = self.x + (self.width-(16 * xs)) -12
            jngl.drawScaled(self.fire[int(self.animation)], x, y, xs, ys)
    def handleCollision(self, player):
        if self.active:
            player.kill()

class Trampoline(GameObject):
    img = RESOURCEWORLD + "spring2.png"
    width = jngl.getWidth(img)
    height = jngl.getHeight(img)
    max_acceleration = -15
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collides = False
        self.scalefactor = 1
        self.strength = 2.2
        self.snd_play = False
    
    def initGame(self, game):
        GameObject.initGame(self, game)
        self.snd_play = False
        
    def handleCollision(self, player):
        if not self.game.checkBoxCollision(player):
            self.collides = True
            self.scalefactor = 0.3
            if player.yspeed > 0.2:
                self.snd_play = True
                player.yspeed -= player.yspeed*self.strength
                if player.yspeed < self.max_acceleration:
                    player.yspeed = self.max_acceleration
    
    def drawPreview(self):
        self.draw()
        
    def draw(self):
        #jngl.draw(self.img, self.x, self.y)
        y = self.y - self.height * (self.scalefactor - 1)
        jngl.drawScaled(self.img, self.x, y+3, 1, self.scalefactor)
    
    def step(self):
        if self.collides:
            if self.snd_play:# and not jngl.isPlaying(SOUND+"trampoline.ogg"):
                self.snd_play = False
                jngl.play(SOUND+"trampoline.ogg")
        self.collides = False
        if self.scalefactor < 1:
            self.scalefactor += 0.1

if __name__ == "__main__":
    import main
    #import LevelEditor
