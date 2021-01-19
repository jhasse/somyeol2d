import jngl
import Map as map
import Somyeol
import GameObjects
import GameObject
from GameObjects import RESOURCEWORLD
from tkinter.filedialog import *
import tkinter
import random
import copy
import Sound
import HighScore
import os
import time
import gc

#disable garbage-collection to get better performance
gc.disable()

HELPSCREEN = "img/World/helpscreen.png"
MIN_FPS = 10

def canvas(x, y, selected, i, free, folder):
    jngl.pushMatrix()
    jngl.translate(x + 60, y + 80)
    if selected:
        factor = jngl.getTime() * 5.0 % 10
        if factor >= 5:
            factor = 5-(factor-5)
        jngl.scale(0.9 + factor/40.0)
    jngl.draw("img/World/canvas.png", -60, -80)
    if free:
        jngl.draw("img/gadgets/forbidden_bg.png", -90, -110)
        jngl.print(str(i+1), -60, -80)
        jngl.draw("img/gadgets/forbidden.png", -90, -110)
    else:
        jngl.print(str(i+1), -60, -80)
    if os.path.isfile("data/maps/"+ folder +"/"+ str(i+1) +".png"):
        jngl.draw("data/maps/"+ folder +"/"+ str(i+1) +".png", -20, -20)
    else:
        jngl.draw("img/World/spawner_2.png", -40, -60)
    jngl.popMatrix()

def canvas_preview(x, y, selected, i, free, folder):
    jngl.pushMatrix()
    jngl.translate(x + 50, y + 80)
    if selected:
        factor = jngl.getTime() * 5.0 % 10
        if factor >= 5:
            factor = 5-(factor-5)
        jngl.scale(0.9 + factor/40.0)
    jngl.draw("img/World/canvas_preview.png", -60, -80)
    if free:
        jngl.draw("img/gadgets/forbidden_bg.png", -90, -110)
        jngl.print(str(i+1), -60, -80)
        jngl.draw("img/gadgets/forbidden.png", -90, -110)
    else:
        jngl.print(str(i+1), -60, -80)
    if os.path.isfile("data/maps/"+ folder +"/"+ str(i+1) +".png"):
        jngl.draw("data/maps/"+ folder +"/"+ str(i+1) +".png", -20, -20)
    else:
        jngl.draw("img/World/spawner_2.png", -40, -60)
    jngl.popMatrix()

def bouncingEnterButton(x, y):
    jngl.pushMatrix()
    jngl.translate(x + 60, y + 80)
    factor = jngl.getTime() * 5.0 % 10
    if factor >= 5:
        factor = 5-(factor-5)
    jngl.scale(0.8 + factor/20.0)
    jngl.draw("img/World/enter.png", -60, -80)
    jngl.popMatrix()

def bouncingButton(x, y, img = "img/World/enter.png" ):
    jngl.pushMatrix()
    jngl.translate(x + 60, y + 80)
    factor = jngl.getTime() * 5.0 % 10
    if factor >= 5:
        factor = 5-(factor-5)
    jngl.scale(0.8 + factor/20.0)
    jngl.draw(img, -60, -80)
    jngl.popMatrix()

class Game:
    def __init__(self):
        self.version = "1.1"
        self.running = True
        self.levelNr = 0
        self.level = None
        self.windowWidth = 1024
        self.windowHeight = 768
        self.camerax = 0
        self.cameray = -self.windowHeight
        self.scale = 0.5
        self.finish = False
        self.finish_highscore = False
        self.highscore = None
        self.levelpack = "ggj/"
        self.enable_credits = True
        self.testmode = False
        self.highscore = HighScore.HighScore()
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        self.bounds = GameObject.Collidable()
        self.levelpack_finished = False

        try:
            if (jngl.getDesktopWidth() < 1024) or (jngl.getDesktopHeight() < 600):
                import tkMessageBox
                tkMessageBox.showwarning("Resolution too small!","Your desktop-resolution is smaller than 1024x600. Please be aware that this can lead to graphical bugs")
            self.windowWidth = jngl.getDesktopWidth()
            self.windowHeight = jngl.getDesktopHeight()
            jngl.showWindow("Somyeol2D {0}".format(self.version), self.windowWidth, self.windowHeight, True)
            self.cameray = -self.windowHeight
        #except RuntimeError: # Fullscreen mode not supported?
        except:
            jngl.showWindow("Somyeol2D {0}".format(self.version), self.windowWidth, self.windowHeight)
##        self.windowWidth = 1024
##        self.windowHeight = 600
##        jngl.showWindow("Somyeol2D {0}".format(self.version), self.windowWidth, self.windowHeight)
        jngl.setBackgroundColor(jngl.Color(144, 187, 227))
        jngl.setAntiAliasing(True)
        jngl.setFont("data/Japestyle Plain.ttf")
        jngl.setFontSize(20)
        self.sound = Sound.Sound(self)

    def setMap(self, map):
        self.level = map
        for obj in (self.level.somyeols + self.level.objects):
            obj.initGame(self)
        self.level.initGame(self)

    def loadNextLevel(self):
        #do garbage-collection here
        gc.collect()
        try:
            self.levelNr += 1
            m = map.Map()
            m.loadLevel("data/maps/{0}{1}.slv".format(self.levelpack, self.levelNr))
            self.setMap(m)
            self.finish = False
            self.finish_highscore = False
            return True
        except:
            self.showCredits()
            return False

    music = [ "sound/somyeol1.ogg", "sound/somyeol2.ogg" ]
    currentTrack = 0
    def checkMusic(self):
        if not jngl.isPlaying(self.music[self.currentTrack]):
            self.currentTrack = (self.currentTrack + 1) % len(self.music)
            jngl.play(self.music[self.currentTrack])

    def moveCamera(self):
        if len(self.level.somyeols) != 0:
            self.minX = None
            self.minY = None
            self.maxX = None
            self.maxY = None
            for somyeol in self.level.somyeols:
                if self.minX == None:
                    self.minX = self.maxX = somyeol.x
                    self.minY = self.minY = somyeol.y
                if self.minX == None or somyeol.x < self.minX:
                    self.minX = somyeol.x
                if self.minY == None or somyeol.y < self.minY:
                    self.minY = somyeol.y
                if self.maxX == None or somyeol.x > self.maxX:
                    self.maxX = somyeol.x
                if self.maxY == None or somyeol.y > self.maxY:
                    self.maxY = somyeol.y
            border = self.windowHeight/1.5
            self.bounds.x = self.minX - 50
            self.bounds.y = self.minY - 50
            self.bounds.width = self.maxX - self.minX + 150
            self.bounds.height = self.maxY - self.minY + 150

            minX = self.minX - border
            minY = self.minY - (border / 2.0)
            maxX = self.maxX + border
            maxY = self.maxY + (border * 1.5)
            self.camerax += (-minX - self.camerax) / 50.0
            self.cameray += (-minY - self.cameray) / 50.0
            if (maxX - minX) < self.windowWidth / self.scale and (maxY - minY) < self.windowHeight / self.scale:
                self.scale += 0.004
            if (maxX - minX) > self.windowWidth / self.scale or (maxY - minY) > self.windowHeight / self.scale:
                self.scale -= 0.004

        if self.cameray < -(self.windowHeight - self.windowHeight / self.scale): # Kamera unter dem Boden?
            self.cameray = -(self.windowHeight - self.windowHeight / self.scale)

    def calculateCollisionBounds(self):
        for gameObject in self.level.objects:
            gameObject.canCollide = False
            if gameObject.checkCollision(self.bounds):
                gameObject.canCollide = True

    def checkBoxCollision(self, somyeol):
        for gameObject in self.level.objects:
            if gameObject.canCollide and gameObject.isBox() and gameObject.checkCollision(somyeol):
                return True
        return False

    def checkCollision(self, somyeol):
        for obj in self.level.objects:
            if obj.canCollide and obj.checkCollision(somyeol):
                obj.handleCollision(somyeol)

    def showCredits(self):
        self.levelpack_finished = True
        if not self.enable_credits:
            self.sound.stopSounds()
            self.running = False
        SHOWCOUNT = 400
        showcount = SHOWCOUNT
        line = 0
        hcount = 0
        SPACE = 60
        lastTime = jngl.getTime()
        timePerStep = 0.01
        credits = [["Programming", "Jannik Waschkau", "Jan-Niklas Hasse", "Kolja Lubitz", "Carsten Pfeffer"],
            ["Leveldesign", "Jannik Waschkau", "Jan-Niklas Hasse", "Kolja Lubitz"],
            ["Graphics", "Carsten Pfeffer", "Kolja Lubitz","Jan-Niklas Hasse"],
            ["Music & Sound","Jannik Waschkau"],
            ["Graphics Engine (JNGL)","Jan-Niklas Hasse"],
            ["Thanks to","Hendrik Leibrandt","Malte 'MonkZ' Kuhn","Anika 'Chibi' Roosch","University Bremen"],
            ["Thanks to","Adrian Lubitz","Jannis Tanner"]]
        jngl.swapBuffers()
        jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
        jngl.updateInput()
        jngl.setFontSize(50)
        while self.running:
            if jngl.getTime() - lastTime > timePerStep:
                lastTime += timePerStep
                jngl.setFontSize(50)
                for i in range(0, 3):
                    jngl.draw(RESOURCEWORLD + "Background.png", i*jngl.getWidth(RESOURCEWORLD + "Background.png"), 0)
                if line >= len(credits):
                    jngl.print("Thanks for Playing!!!", int((self.windowWidth/2) - jngl.getTextWidth("Thanks for Playing") / 2), (self.windowHeight/2))
                    self.levelpack_finished = True
                    if jngl.keyPressed(jngl.key.Any):
                        self.sound.stopSounds()
                        self.running = False
                elif jngl.keyPressed(jngl.key.Any):
                    line +=1
                else:
                    for word in credits[line]:
                        jngl.print(word, int((self.windowWidth/2) - jngl.getTextWidth(word) / 2), (self.windowHeight/2)-150+SPACE*hcount)
                        hcount += 1
                    hcount = 0
                    showcount-=1
                    if not showcount:
                        line+=1
                        showcount = SHOWCOUNT
                jngl.setFontSize(20)
                jngl.print("www.somyeol.com", self.windowWidth-180, self.windowHeight-30)
                jngl.swapBuffers()
                jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
                jngl.updateInput()


    def run(self):
        self.levelpack_finished = False
        self.highscore.loadHighscore(self.levelpack)
        self.levelpack_finished = False
        lastTime = jngl.getTime()
        needDraw = True
        timePerStep = 0.01
        counter = 0
        fps = 0
        start_time = time.time()
        seconds = 0
        min_fps_count = MIN_FPS
        self.moveCamera()
        while self.running:
            if min_fps_count and jngl.getTime() - lastTime > timePerStep:
                lastTime += timePerStep
                needDraw = True
                if jngl.keyPressed(jngl.key.Escape):
                    self.sound.stopSounds()
                    self.running = False
                if jngl.keyPressed("r"):
                    self.level.somyeols = []
                    self.level.points = 0

                self.moveCamera()
                self.calculateCollisionBounds()
                if not self.finish:
                    self.level.step()
                else:
                    for a in self.level.animations:
                        a.step(self.level.animations)
                    for o in self.level.objects:
                        o.step()

            elif needDraw:
                if not min_fps_count:
                    lastTime = jngl.getTime()
                min_fps_count = MIN_FPS
                self.sound.playSounds()
                self.checkMusic()
                jngl.setFontSize(20)
                needDraw = False

                self.level.drawBackground(self.cameray)
                jngl.pushMatrix()
                jngl.translate(self.windowWidth/2, self.windowHeight)
                jngl.scale(1 + (self.scale - 1) / 2)
                jngl.translate(self.camerax / 2, -self.windowHeight + self.cameray / 2)
                for i in range(-2, 3):
                    jngl.draw(RESOURCEWORLD + "mountains.png", i*1024, self.windowHeight-300)
                jngl.popMatrix()
                jngl.pushMatrix()
                jngl.scale(self.scale)
                jngl.translate(self.camerax, self.cameray)
                self.level.draw()
                #uncomment for visualization of boundingbox
##                jngl.setColor(255,0,0,150)
##                jngl.drawRect(self.bounds.x,self.bounds.y,self.bounds.width,self.bounds.height)
                jngl.popMatrix()

                jngl.pushSpriteAlpha(150)
                jngl.draw("img/World/canvas.png", -80, -100)
                jngl.print("Somyeols: {0}".format(len(self.level.somyeols)), 10, 10)
                jngl.draw("img/World/canvas.png", self.windowWidth - 200, -120)
                jngl.print("Level: {0}".format(self.levelNr), self.windowWidth - 140, 10)
                jngl.popSpriteAlpha()

                jngl.print("Time: %.2f"%(seconds), 10, 40)

                if self.finish:
                    if not self.testmode:
                        def printCentered(t, x, y):
                            jngl.print(t, int(x-jngl.getTextWidth(t) / 2), y)

                        def printHighscore():
                            x,y = (self.windowWidth/2) - 207, (self.windowHeight/2) - 140
                            jngl.draw("img/World/highscore.png", x,y)
                            hs = self.highscore.getLevelScore(self.levelNr)
                            jngl.print("#".format(len(self.level.somyeols)), x+30, y+80)
                            jngl.print("Score".format(len(self.level.somyeols)), x+100, y+80)
                            jngl.print("Seconds".format(len(self.level.somyeols)), x+200, y+80)
                            jngl.print("Rank".format(len(self.level.somyeols)), x+300, y+80)
                            i = 1
                            best_rank = hs[0].getRank()
                            for score in hs:
                                jngl.setFontColor(0,0,0)
                                if new_score:
                                    if new_score == score:
                                        jngl.setFontColor(255,50,50)
                                jngl.print(str(i)+".", x+30, y+90+(30*i))
                                #jngl.print(str(score.score), x+120, y+90+(30*i))
                                jngl.print("{0}".format(score.score), x+100, y+90+(30*i))
                                jngl.print("{0:.2f}".format(score.time), x+200, y+90+(30*i))
                                jngl.print("{0:.2%}".format(score.getRank()/best_rank), x+300, y+90+(30*i))
                                i += 1
                            jngl.setFontColor(0,0,00)
                        if self.finish_highscore:
                            printHighscore()
                        else:
                            x,y = (self.windowWidth/2) - (jngl.getWidth("img/World/canvas.png")/2), (self.windowHeight/2) - (jngl.getHeight("img/World/canvas.png")/2)
                            jngl.draw("img/World/canvas.png", self.windowWidth/2 - 137, self.windowHeight/2 - 92)
                            printCentered("FINAL SCORE", x+(jngl.getWidth("img/World/canvas.png")/2), y+20)
                            printCentered("NEEDED: 100", x+(jngl.getWidth("img/World/canvas.png")/2), y+140)
                            jngl.setFontSize(50)
                            printCentered(str(self.level.points), x+(jngl.getWidth("img/World/canvas.png")/2), y+70)
                        bouncingEnterButton(x+50, y+jngl.getHeight("img/World/canvas.png")+50)
                        if jngl.keyPressed(jngl.key.Return) and self.finish_highscore:
                            self.levelpack_finished = not self.loadNextLevel()
                            start_time = time.time()

                        elif jngl.keyPressed(jngl.key.Return):
                            if self.level.points < self.level.needed_points:
                                self.levelNr -= 1
                                self.levelpack_finished = not self.loadNextLevel()
                                start_time = time.time()
                            else:
                                self.finish_highscore = True
                                # HIGHSCORE
                                new_score = self.highscore.newHighscore(self.levelNr, seconds, self.level.points)
                                if new_score:
                                    self.highscore.saveHighscore(self.levelpack)
                                time.sleep(.5)
                    else:self.running=False
                else:
                    seconds = time.time()-start_time

                fps += jngl.getFPS() / 50
                counter -= 1
                if counter < 0:
                    counter = 50
                    jngl.setTitle("Somyeol2D {0} - FPS: {1}".format(self.version, int(fps)))
                    fps = 0
                jngl.setFontSize(20)
                jngl.print("Press F1 for Help", 10, self.windowHeight-30)
                if jngl.keyDown(jngl.key.F1):
                    jngl.draw(HELPSCREEN, (self.windowWidth/2)-jngl.getWidth(HELPSCREEN)/2, (self.windowHeight/2)-jngl.getHeight(HELPSCREEN)/2)

                #uncomment for visualization of collision-count
                #colcount = 0
                #for o in self.level.objects:
                #    if o.canCollide:
                #        colcount+=1
                #jngl.print(str(colcount), self.windowWidth-680, self.windowHeight-50)
                jngl.print("www.somyeol.com", self.windowWidth-180, self.windowHeight-30)

                jngl.swapBuffers()
                jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
                jngl.updateInput()
            else:
                jngl.sleep(1)
            min_fps_count-=1
        self.sound.stopSounds()
if __name__ == '__main__':
    import main
