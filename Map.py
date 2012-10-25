# -*- coding: utf-8 -*-
##############################################################
##
##############################################################

import jngl
import cPickle
import GameObjects

from tkFileDialog import *
import Tkinter

from GameObjects import RESOURCEWORLD
SOUND = "sound/"
class Map(object):
    sound_win = [SOUND+"win1.ogg",SOUND+"win2.ogg",SOUND+"win3.ogg"]
    sound_loose = [SOUND+"loose1.ogg",SOUND+"loose2.ogg",SOUND+"loose3.ogg",
        SOUND+"loose4.ogg",SOUND+"loose5.ogg",SOUND+"loose6.ogg"]
    sound_perfect = [SOUND+"eifel_tower1.ogg"]
    def __init__(self):
        self.somyeols = []
        self.objects = []
        self.images = []
        self.animations= []
        self.points = 0
        self.needed_points_perfect = 500
        self.needed_points = 100

    def initGame(self, game):
        self.game = game

    def drawBackground(self, cameray):
        for i in range(0, 3):
            jngl.draw(RESOURCEWORLD + "Background.png", i*jngl.getWidth(RESOURCEWORLD + "Background.png"), 0)
        jngl.draw(RESOURCEWORLD + "Wolken2.png", -350 + (jngl.getTime() * 5) % (self.game.windowWidth+jngl.getWidth(RESOURCEWORLD + "Wolken2.png")+350), 0)
        jngl.draw(RESOURCEWORLD + "Wolken2.png", -450 + (jngl.getTime() * 4) % (self.game.windowWidth+jngl.getWidth(RESOURCEWORLD + "Wolken2.png")+450), 100)
        jngl.draw(RESOURCEWORLD + "Wolken2.png", -650 + (jngl.getTime() * 3) % (self.game.windowWidth+jngl.getWidth(RESOURCEWORLD + "Wolken2.png")+650), 200)
        jngl.draw(RESOURCEWORLD + "Wolken2.png", -850 + (jngl.getTime() * 2) % (self.game.windowWidth+jngl.getWidth(RESOURCEWORLD + "Wolken2.png")+850), 150)
        jngl.draw(RESOURCEWORLD + "Wolken2.png", -1050 + (jngl.getTime() * 1) % (self.game.windowWidth+jngl.getWidth(RESOURCEWORLD + "Wolken2.png")+1050), 50)

    def draw(self):
        for image in self.images:
            image.draw()
        for somyeol in self.somyeols:
            somyeol.draw()
        for animation in self.animations:
            animation.draw()
        for object in self.objects:
            object.draw()
    
    def drawEditor(self):
        for image in self.images:
            image.draw()
        for somyeol in self.somyeols:
            somyeol.draw()
        for animation in self.animations:
            animation.draw()
        for object in self.objects:
            object.drawEditor()
            
    def drawPortalLines(self):
        '''
        '''
        already_drawn = []
        for object in self.objects:
            if type(object) == GameObjects.Portal and object not in already_drawn and object.linked:
                already_drawn.append(object.linked)
                jngl.setColor(255, 0, 0, 180)
                jngl.drawLine(object.x+16, object.y+33, object.linked.x+16, object.linked.y+33)
                

    def saveLevel(self, file = None):
        if file == None:
            file = open("test.slv", "wb")
        data = [self.somyeols,self.objects,self.images]
        cPickle.dump(data, file)

    def loadLevel(self, path = None):
        self.points = 0
        if path == None:
            path = askopenfilename(filetypes=[("Somyeol Level", "*.slv")])
        if path == "" or type(path) != str:
            return
        try:
            file = open(path, "rb")
            data = cPickle.load(file)
            self.somyeols = data[0]
            self.objects = data[1]
            self.images = data[2]
        except EOFError:
            return

    def step(self):
        for animation in self.animations:
            animation.step(self.animations)
        for somyeol in self.somyeols:
            somyeol.breath()
            somyeol.move(self.game)
        for object in self.objects:
            object.step()

        if len(self.somyeols) <= 0:
            if self.points >= self.needed_points:
                if self.points >= self.needed_points_perfect:jngl.play(self.game.sound.getSound(self.sound_perfect))
                else: jngl.play(self.game.sound.getSound(self.sound_win))
            else:
                jngl.play(self.game.sound.getSound(self.sound_loose))
            self.game.finish = True

    def checkCollision(self, somyeol):
        return False

    def addPoints(self, points):
        self.points += points

if __name__ == "__main__":
    import main
