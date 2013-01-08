# -*- coding: utf-8 -*-
##############################################################
## This in the Instanze of one Somyeol
##############################################################

import jngl
import random
import GameObject
from GameObjects import RESOURCEWORLD

RESOURCE = "img/Somyeols/"
SOUND = "sound/"

class Somyeol(GameObject.GameObject):

    #The Audio-Files
    sound_jump = [SOUND+"jump1.ogg",SOUND+"jump2.ogg",SOUND+"jump3.ogg",SOUND+"jump4.ogg",
        SOUND+"jump5.ogg",SOUND+"jump6.ogg",SOUND+"jump7.ogg",SOUND+"jump8.ogg",SOUND+"jump9.ogg",
        SOUND+"jump10.ogg",SOUND+"jump11.ogg",SOUND+"jump12.ogg",SOUND+"jump13.ogg"]
    sound_jump_crowd = [SOUND+"jump_crowd.ogg"]
    sound_walk_crowd = [SOUND+"walk_crowd1.ogg",SOUND+"walk_crowd2.ogg",
        SOUND+"walk_crowd3.ogg",SOUND+"walk_crowd4.ogg",
        SOUND+"walk_crowd5.ogg",SOUND+"walk_crowd6.ogg"]
    sound_walk = [SOUND+"walk1.ogg",SOUND+"walk2.ogg",SOUND+"walk3.ogg",
        SOUND+"walk4.ogg",SOUND+"walk5.ogg",SOUND+"walk6.ogg",SOUND+"walk7.ogg",
        SOUND+"walk8.ogg",SOUND+"walk9.ogg",SOUND+"walk10.ogg",SOUND+"walk11.ogg",
        SOUND+"walk12.ogg"]
    sound_dead = [SOUND+"dead1.ogg",SOUND+"dead2.ogg",SOUND+"dead3.ogg",SOUND+"dead4.ogg",SOUND+"dead5.ogg"]
    sound_goal = [SOUND+"goal1.ogg",SOUND+"goal2.ogg",SOUND+"goal3.ogg",SOUND+"goal4.ogg",SOUND+"goal5.ogg"]
    sound_win = [SOUND+"win1.ogg",SOUND+"win2.ogg",SOUND+"win3.ogg"]
    sound_loose = [SOUND+"loose1.ogg",SOUND+"loose2.ogg",SOUND+"loose3.ogg",SOUND+"loose4.ogg",SOUND+"loose5.ogg"]
    sound_land = [SOUND+"land1.ogg",SOUND+"land2.ogg",SOUND+"land3.ogg"]
    filenames = [RESOURCE + "Somyeol_stand_0.png", RESOURCE + "Somyeol_stand_1.png"]
    def getSound(self, list):
        return list[random.randint(0,len(list))-1]

    def __init__(self, x, y):
        self.currentFile = 0
        self.filename = self.filenames[self.currentFile]
        self.animationCnt = 10
        self.width = jngl.getWidth(self.filename)
        self.height = jngl.getHeight(self.filename)
        self.x = x
        self.y = y - 2
        self.yspeed = 0
        self.xspeed = 0
        self.dead = False
        self.canJump = False
        self.nonstopJump = True
        self.points = 10
        self.breathFactor = 1
        self.breathIn = True
        self.hasKey = False
        self.moveSpeed = 0.2
        self.jumpSpeed = 10.25
        self.inverted = False
        self.error_correction_x = 0
        self.error_correction_y = 0

    def initGame(self, game):
        self.game = game
        self.windowWidth = game.windowWidth
        self.windowHeight = game.windowHeight
        self.breathFactor = 1
        self.breathIn = True
        self.error_correction_x = 0
        self.error_correction_y = 0

    def breath(self):
        if self.breathIn:
            self.breathFactor -= 0.005 * random.randint(0,100)/100.0
            if self.breathFactor <= 0.95:
                self.breathIn = not self.breathIn
        else:
            self.breathFactor += 0.005 * random.randint(0,100)/100.0
            if self.breathFactor >= 1.05:
                self.breathIn = not self.breathIn
        
        if abs(self.xspeed) > 0.1:
            self.animationCnt -= abs(self.xspeed) / 3.0
            if self.animationCnt < 0:
                self.animationCnt = 10
                self.currentFile += 1
                self.currentFile = self.currentFile % len(self.filenames)
        else:
            self.currentFile = 0

    def move(self, game):
        self.oldX = self.x
        self.oldY = self.y
        moveSpeed = self.moveSpeed + random.randint(0,5)/100.0
        if self.inverted:
            moveSpeed = -moveSpeed
        if jngl.keyDown(jngl.key.Right):
            self.xspeed += moveSpeed
        if jngl.keyDown(jngl.key.Left):
            self.xspeed -= moveSpeed
        self.yspeed += 0.2
        self.xspeed *= 0.97

        self.x += self.xspeed
        self.y += self.yspeed
        game.checkCollision(self)
        self.y -= self.yspeed
        # For boxes we have to check both direction movements individually
        # since we want to know if we can jump
        if game.checkBoxCollision(self):
            self.x -= self.xspeed + self.error_correction_x
            self.xspeed = -self.xspeed

        self.y += self.yspeed
        if game.checkBoxCollision(self):
            self.y -= self.yspeed  + self.error_correction_y
            if self.yspeed > 0:
                self.jump(game)
            else:
                self.yspeed = -self.yspeed
        else:
            self.canJump = False
        ##Needed to get walking sounds
        #if self.canJump and (self.xspeed > 0.2 or self.xspeed < -0.2):
        #    game.sound.addToQueue(self.getSound(self.sound_walk))
        if self.y + self.height > self.windowHeight:
            self.kill()
        self.error_correction_x = 0
        self.error_correction_y = 0
    def jump(self, game):
        ##Vermutlich nicht notwendig
        #game.checkCollision(self)
        if (jngl.keyDown(jngl.key.Up) or jngl.keyDown(jngl.key.Space)) and self.canJump:
            self.yspeed = -self.jumpSpeed + random.randint(0,5)/10.0
            game.sound.addToQueue(self.getSound(self.sound_jump))
        else:
            ##if self.canJump != True: self.game.sound.sound_queue.add(self.getSound(self.sound_land)) ##Play the landing sound, doesnt work right because it gets called ~4times
            self.canJump = True
            self.yspeed = 0
    def explode(self):
        self.exploding = True
    def drawPreview(self):
        jngl.pushSpriteAlpha(100)
        jngl.draw(self.filename, self.x, self.y)
        jngl.popSpriteAlpha()
    def draw(self):
        jngl.setColor(255, 255, 255)
        x = self.x - self.width * (self.breathFactor - 1) / 2
        y = self.y + self.height * (self.breathFactor - 1)
        xfactor = self.breathFactor
        yfactor = 1+(1-self.breathFactor)
        if self.xspeed >= 0:
            jngl.drawScaled(self.filenames[self.currentFile], x, y, xfactor, yfactor)
        else:
            jngl.drawScaled(self.filenames[self.currentFile], x + self.width, y, -xfactor, yfactor)
        if self.hasKey:
            jngl.draw(RESOURCEWORLD + "key.png", self.x, self.y - 20)
    def kill(self):
        if self in self.game.level.somyeols:
            self.game.sound.addToQueue(self.getSound(self.sound_dead))
            self.game.level.somyeols.remove(self)
            from DeathAnimation import DeathAnimation
            self.game.level.animations.append(DeathAnimation(self.x + self.width / 2, self.y + self.height / 2))

    def goal(self):
        if self in self.game.level.somyeols:
            self.game.level.somyeols.remove(self)
            self.game.level.addPoints(self.points)
            self.game.sound.addToQueue(self.getSound(self.sound_goal))
    
    def __str__(self):
        return self.__class__.__name__

class InvertedSomyeol(Somyeol):
    filenames = [RESOURCE + "InvertedSomyeol_stand_0.png", RESOURCE + "InvertedSomyeol_stand_1.png"]
    def __init__(self,x,y):
        Somyeol.__init__(self,x,y)
        self.filename = self.filenames[0]
        self.points = 15
        self.inverted = True

class FatSomyeol(Somyeol):
    sound_dead = [SOUND+"fat_dead1.ogg"]
    sound_goal = [SOUND+"fat_goal1.ogg"]
    sound_jump = [SOUND+"fat_jump1.ogg",SOUND+"fat_jump2.ogg",SOUND+"fat_jump3.ogg"]
    filenames = [RESOURCE + "FatSomyeol_small_0.png", RESOURCE + "FatSomyeol_small_1.png"]
    def __init__(self,x,y):
        Somyeol.__init__(self,x,y)
        self.currentFile = 0
        self.filename = self.filenames[self.currentFile]
        self.width = jngl.getWidth(self.filename)
        self.height = jngl.getHeight(self.filename)
        self.points = 50
        self.moveSpeed = 0.1
        self.jumpSpeed = 6

class CrippleSomyeol(Somyeol):
    sound_jump = [SOUND+"cripple_jump1.ogg",SOUND+"cripple_jump2.ogg"]
    filenames = [RESOURCE + "CrippleSomyeol_small_0.png", RESOURCE + "CrippleSomyeol_small_1.png"]
    def __init__(self,x,y):
        Somyeol.__init__(self,x,y)
        self.filename = self.filenames[self.currentFile]
        self.points = 25

    def jump(self, game):
        self.yspeed = 0
        if (jngl.keyDown(jngl.key.Up)):
            self.game.sound.addToQueue(self.getSound(self.sound_jump))

class EvilSomyeol(Somyeol):
    sound_dead = [SOUND+"evil_dead1.ogg",SOUND+"evil_dead1.ogg"]
    sound_goal = [SOUND+"evil_goal1.ogg"]
    sound_jump = [SOUND+"evil_jump1.ogg",SOUND+"evil_jump2.ogg",SOUND+"evil_jump3.ogg"]
    filenames = [RESOURCE + "EvilSomyeol_small_0.png", RESOURCE + "EvilSomyeol_small_1.png"]
    def __init__(self,x,y):
        Somyeol.__init__(self,x,y)
        self.filename = self.filenames[0]
        self.points = -100

class SmallSomyeol(Somyeol):
    filenames = [RESOURCE + "small_Somyeol_small_0.png", RESOURCE + "small_Somyeol_small_1.png"]
    def __init__(self,x,y):
        Somyeol.__init__(self,x,y)
        self.filename = self.filenames[0]
        self.points = 5
        self.filename = self.filenames[self.currentFile]
        self.width = jngl.getWidth(self.filename)
        self.height = jngl.getHeight(self.filename)
        
class GhostSomyeol(Somyeol):
    def __init__(self,x,y):
        Somyeol.__init__(self,x,y)
        self.collidable = GameObject.Collidable()
    
    def initGame(self,game):
        Somyeol.initGame(self,game)
        self.collidable = GameObject.Collidable()
        self.collidable.x = self.x
        self.collidable.y = self.y + self.height
        self.collidable.width = self.width
        self.collidable.height = 1
    
    def drawPreview(self):
        jngl.setSpriteColor(100, 100, 255, 20)
        jngl.draw(self.filename, self.x, self.y)
        jngl.setSpriteColor(255, 255, 255, 255)
    
    def draw(self):
        jngl.setSpriteColor(100,100,255,100)
        Somyeol.draw(self)
        jngl.setSpriteColor(255,255,255,255)
        
    def move(self, game):
        self.oldX = self.x
        self.oldY = self.y
        moveSpeed = self.moveSpeed + random.randint(0,5)/100.0
        if self.inverted:
            moveSpeed = -moveSpeed
        if jngl.keyDown(jngl.key.Right):
            self.xspeed += moveSpeed
        if jngl.keyDown(jngl.key.Left):
            self.xspeed -= moveSpeed
        self.yspeed += 0.2
        self.xspeed *= 0.97

        self.x += self.xspeed
        #self.y += self.yspeed
        #game.checkCollision(self)
        #self.y -= self.yspeed
        # For boxes we have to check both direction movements individually
        # since we want to know if we can jump
        #if game.checkBoxCollision(self):
        #   self.x -= self.xspeed
        #   self.xspeed = -self.xspeed
        self.y += self.yspeed
        game.checkCollision(self)
        self.collidable.x = self.x
        self.collidable.y = self.y + self.height
        if game.checkBoxCollision(self.collidable):
            if self.yspeed > 0:            
                self.y -= self.yspeed + self.error_correction_y    
            self.jump(game)
            
            #if self.yspeed >= 0:
            #    self.jump(game)
            #else:
            #    self.yspeed = -self.yspeed
        else:
            self.canJump = False
        ##Needed to get walking sounds
        #if self.canJump and (self.xspeed > 0.2 or self.xspeed < -0.2):
        #    game.sound.addToQueue(self.getSound(self.sound_walk))
        if self.y + self.height > self.windowHeight:
            self.kill()
        self.error_correction_x = 0
        self.error_correction_y = 0
if __name__ == "__main__":
    import main
