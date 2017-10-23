# -*- coding: utf-8 -*-
import jngl
import Map
import Somyeol
import GameObjects
import six.moves.cPickle
import inspect
import os
import copy
import random
from Image import Image

from tkinter.filedialog import *
import tkinter.messagebox as tkMessageBox
import tkinter

class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 1
        self.height = 1

class LevelEditor(object):
    gridSize = 32

    def showWindow(self):
        try:
            jngl.showWindow("Somyeol2D {0}".format(self.version), jngl.getDesktopWidth(), jngl.getDesktopHeight(), True)
            self.windowWidth = jngl.getDesktopWidth()
            self.windowHeight = jngl.getDesktopHeight()
            self.cameray = -self.windowHeight
        #except RuntimeError: # Fullscreen mode not supported?
        except:
            jngl.showWindow("Somyeol2D {0}".format(self.version), self.windowWidth, self.windowHeight)

        #jngl.showWindow("Somyeol2D - LevelEditor {0}".format(self.version), self.windowWidth, self.windowHeight,False)
        jngl.setBackgroundColor(255, 255, 255)
        jngl.setAntiAliasing(True)
        jngl.cancelQuit()

    def __init__(self):
        self.version = "1.1"
        self.camerax = 0
        self.cameray = 0
        self.level = Map.Map()
        self.gridEnabled = True
        self.add10 = False
        self.scale = 1
        self.windowWidth = 1024
        self.windowHeight = 600
        self.zoom = False
        try:
            if jngl.getDesktopWidth() < 1024 or jngl.getDesktopHeight() < 768:
                import tkMessageBox
                tkMessageBox.showwarning("Resolution too small!","Your desktop-resolution is smaller than 1024x768. Please be aware that this can lead to graphical bugs")
            self.windowWidth = jngl.getDesktopWidth()
            self.windowHeight = jngl.getDesktopHeight()
        except:
            pass
        self.showWindow()
        self.placeable = []
        self.placeable_count = 0
        self.quickselect = ["0","1","2","3","4","5","6","7","8","9",jngl.key.F1,
        jngl.key.F2,jngl.key.F3,jngl.key.F4,jngl.key.F5,jngl.key.F6,jngl.key.F7,
        jngl.key.F8,jngl.key.F9,jngl.key.F10,jngl.key.F11,jngl.key.F12]


        #Generate the list if placeables
        for name, obj in inspect.getmembers(Somyeol, inspect.isclass):
            if name != "GameObject":
                self.placeable.append(obj)

        for name, obj in inspect.getmembers(GameObjects,  inspect.isclass):
            if name != "GameObject":
                self.placeable.append(obj)

    def addImage(self, x, y):
        path = askopenfilename(initialdir="img/gadgets", filetypes=[("PNG Image", "*.png")])
        if path != "":
            fileName = str("img/gadgets/" + os.path.split(path)[1])
            try:
                jngl.load(fileName)
                self.level.images.append(Image(x, y, fileName))
            except RuntimeError as e:
                jngl.errorMessage("{0}. It must be inside img/gadgets/ folder.\n{1}".format(e, fileName))

    def getObjectAt(self, x, y):
        mouse = Mouse(x, y)
        for gameObject in self.level.objects:
            if gameObject.checkCollision(mouse):
                return gameObject
        for somyeol in self.level.somyeols:
            if somyeol.checkCollision(mouse):
                return somyeol
        for image in self.level.images:
            if image.checkCollision(mouse):
                return image

    def addObject(self, x, y):
        #If its a Somyeol...
        if self.placeable[self.placeable_count].__module__ == Somyeol.Somyeol.__module__:
            if self.add10:
                for i in range(0, 10):
                    self.level.somyeols.append(self.placeable[self.placeable_count](x + random.randint(0, 20) - 10,y + random.randint(0, 20) - 10))
            else:
                somyeol = self.placeable[self.placeable_count](x,y)
                self.level.somyeols.append(somyeol)

        #If its a Box...
        elif self.placeable[self.placeable_count] == GameObjects.Box or self.placeable[self.placeable_count] == GameObjects.MovingBox or self.placeable[self.placeable_count] == GameObjects.InvisibleBox or self.placeable[self.placeable_count] == GameObjects.FragileBox or self.placeable[self.placeable_count] == GameObjects.PassableBox or self.placeable[self.placeable_count] == GameObjects.PulsatingBox:
            #Starting Position
            if not self.box: self.box = [x,y]
            #If the starting Position is set, draw the box
            else:
                if self.placeable[self.placeable_count] == GameObjects.Box or self.placeable[self.placeable_count] == GameObjects.InvisibleBox or self.placeable[self.placeable_count] == GameObjects.FragileBox or self.placeable[self.placeable_count] == GameObjects.PassableBox or self.placeable[self.placeable_count] == GameObjects.PulsatingBox:
                    self.box = self.placeable[self.placeable_count](self.box[0],self.box[1],x-self.box[0],y-self.box[1])
                    self.level.objects.append(self.box)
                    self.box = None
                if self.placeable[self.placeable_count] == GameObjects.MovingBox:
                    if len(self.box) == 2:
                        self.box = self.box + [x,y]
                    else:
                        if x-self.box[2] <0:
                            x+=self.box[2]-self.box[0]
                        self.box = self.placeable[self.placeable_count](self.box[0],self.box[1],self.box[2]-self.box[0],self.box[3]-self.box[1],x-self.box[2],y-self.box[3])
                        self.level.objects.append(self.box)
                        self.box = None

        else:
            object = self.placeable[self.placeable_count](x,y)
            self.level.objects.append(object)

    def moveObject(self, x, y):
        if self.obj:
            self.obj.x = x - self.obj.width / 2
            self.obj.y = y - self.obj.height / 2
        else:
            self.obj = self.getObjectAt(x, y)

    def run(self):
        self.camera = 0
        lastTime = jngl.getTime()
        needDraw = True
        timePerStep = 0.01
        counter = 0
        fps = 0
        self.box = None
        self.port1 = None

        while jngl.running():
            jngl.updateInput()

            x = jngl.getMouseX() - self.camerax
            y = jngl.getMouseY() - self.cameray
            if self.gridEnabled:
                x = int(x/self.gridSize)*self.gridSize
                y = int(y/self.gridSize)*self.gridSize
                if self.box:
                    x += self.gridSize
                    y += self.gridSize
            if jngl.getTime() - lastTime > timePerStep:
                lastTime += timePerStep
                needDraw = True
                if jngl.keyDown("z"):
                    if not self.zoom:
                        self.camerax += self.windowWidth/2
                        self.cameray += self.windowHeight/2
                        self.zoom = True
                    #self.gridEnabled = False
                    self.scale = 0.5
                elif self.zoom:
                    self.zoom = False
                    self.camerax -= self.windowWidth/2
                    self.cameray -= self.windowHeight/2
                jngl.scale(self.scale)
                self.scale = 1
                if jngl.keyPressed("s"):# and jngl.keyDown(jngl.key.ControlL):
                    jngl.hideWindow()
                    file = asksaveasfile(mode='wb', defaultextension='.slv', filetypes=[("Somyeol Level", "*.slv")])
                    if file != None:
                        self.level.saveLevel(file)
                        file.close()
                    self.showWindow()

                if jngl.keyPressed("g"):
                    self.toggleGrid()

                if jngl.keyPressed(jngl.key.ControlL) and jngl.keyPressed("n"):
                    self.camerax = 0
                    self.cameray = 0
                    self.level = Map.Map()
                    self.gridEnabled = True
                    self.add10 = False
                    self.scale = 1
                    self.zoom = False

                if jngl.keyPressed("l"):# and jngl.keyDown(jngl.key.ControlL):
                    jngl.hideWindow()
                    self.level.loadLevel()
                    self.showWindow()

                if jngl.keyPressed("i"):
                    self.addImage(x, y)

                if jngl.keyPressed("t"):
                    jngl.hideWindow()
                    from Game import Game
                    game = Game()
                    tempMap = copy.deepcopy(self.level)
                    game.setMap(tempMap)
                    game.enable_credits = False
                    game.testmode=True
                    game.run()
                    jngl.hideWindow()
                    self.showWindow()
                if jngl.keyPressed("m"):
                    self.add10 = not self.add10

                #Change the Placeable
                if jngl.mousePressed(jngl.mouse.Right) or jngl.keyPressed(jngl.key.PageUp):
                    self.box = None
                    self.port1 = None
                    self.placeable_count += 1
                    if self.placeable_count >= len(self.placeable):
                        self.placeable_count = 0

                if jngl.keyPressed(jngl.key.PageDown):
                    self.box = None
                    self.port1 = None
                    self.placeable_count -= 1
                    if self.placeable_count < 0:
                        self.placeable_count = len(self.placeable)-1

                for i in range (len(self.quickselect)-1):
                    if (jngl.keyPressed(self.quickselect[i])):
                        self.box = None
                        self.port1 = None
                        self.placeable_count = i % (len(self.placeable))

                if jngl.mousePressed(jngl.mouse.Middle) or jngl.keyPressed(jngl.key.Delete):
                    obj = self.getObjectAt(x, y)
                    lists = (self.level.somyeols, self.level.objects, self.level.images)
                    for l in lists:
                        if obj in l:
                            l.remove(obj)

                if jngl.keyDown(jngl.key.ShiftL) or jngl.keyDown(jngl.key.ShiftR):
                    if jngl.mouseDown(jngl.mouse.Left):
                        self.moveObject(x, y)
                else:
                    self.obj = None
                    if jngl.mousePressed(jngl.mouse.Left):
                        self.addObject(x, y)

                if jngl.keyDown(jngl.key.Right):
                    self.camerax -= 4
                if jngl.keyDown(jngl.key.Left):
                    self.camerax += 4
                if jngl.keyDown(jngl.key.Up):
                    self.cameray += 4
                if jngl.keyDown(jngl.key.Down):
                    self.cameray -= 4

                if (self.cameray / self.scale + self.windowHeight) * self.scale <= self.windowHeight: # Kamera immer über dem Boden?
                    self.cameray = (self.windowHeight / self.scale - self.windowHeight) * self.scale

                if jngl.keyPressed(jngl.key.Escape):
                    jngl.hideWindow()
                    quit = tkMessageBox.askyesno("Close Editor?","Do you really want to quit?")
                    if quit:
                        return
                    self.showWindow()
                    jngl.swapBuffers()

            elif needDraw:
                needDraw = False
                jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
                jngl.pushMatrix()
                jngl.translate(self.camerax, self.cameray)
                self.level.drawEditor()
                if not self.zoom:
                    if not jngl.keyDown(jngl.key.ShiftL) and not jngl.keyDown(jngl.key.ShiftR):
                        self.placeable[self.placeable_count](x, y).drawPreview()
                        jngl.print(self.placeable[self.placeable_count](x,y).__str__(),x + 40 ,y )
                        if self.add10:
                            jngl.print("10x", x - 40, y + 10)
                    if self.box:
                        jngl.setColor(100, 100, 100, 100)
                        if len(self.box) > 2:
                            jngl.setColor(255, 100, 100, 100)
                        jngl.drawRect(self.box[0], self.box[1], x - self.box[0], y - self.box[1])
                    elif self.port1:
                        jngl.setColor(255, 50, 50, 100)
                        jngl.drawLine(self.port1.x+16, self.port1.y+33, x+16, y+33)

                jngl.popMatrix()
                jngl.pushMatrix()
                jngl.translate(self.camerax % self.gridSize, self.cameray % self.gridSize)
                if self.gridEnabled and not self.zoom:
                    jngl.setColor(0, 0, 0, 40)
                    for x in range(0, self.windowWidth, self.gridSize):
                        jngl.drawLine(x, -self.gridSize, x, self.windowHeight)
                    for y in range(0, self.windowHeight, self.gridSize):
                        jngl.drawLine(-self.gridSize, y, self.windowWidth, y)
                jngl.popMatrix()
                jngl.setFontColor(0,0,0, 200)
                if jngl.keyDown('h'):
                    jngl.print("L - load file\nS - save file\nI - insert image\nLeft Mouse Button - add object\nMiddle Mouse Button - remove object\nRight Mouse Button or Page Up/Down - change object to add\nShift + Left Mouse Button - Move object\nG - change grid size\nT - test level\nM - add 10 somyeols at once\nZ Zoom out\nCtrl+N New Level (deletes everything!)", 10, 10)
                else:
                    jngl.print("Press H to show help text.   X = {0}   Y = {1}".format(-self.camerax, self.cameray), 10, 10)
                jngl.print("Somyeols: {0} Objects: {1}".format(len(self.level.somyeols), len(self.level.objects)), 10, 30)
                fps += jngl.getFPS() / 50
                counter -= 1
                if counter < 0:
                    counter = 50
                    jngl.setTitle("Somyeol2D - LevelEditor {0} - FPS: {1}".format(self.version, int(fps)))
                    fps = 0
                jngl.swapBuffers()
            else:
                jngl.sleep(1)

    def toggleGrid(self):
        if self.gridEnabled:
            if self.gridSize < 64:
                self.gridSize *= 2
            else:
                self.gridEnabled = False
        else:
            self.gridEnabled = True
            self.gridSize = 16

#if __name__ == "__main__":
root = tkinter.Tk()
root.withdraw()
game = LevelEditor()
game.run()
jngl.hideWindow()
