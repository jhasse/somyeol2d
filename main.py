#!/usr/bin/env python3

import jngl
import os
from tkinter.filedialog import *
import tkinter
##import cProfile
from Game import Game, bouncingEnterButton, bouncingButton, canvas_preview
HELPSCREEN = "img/World/helpscreen.png"

OVERFLOW_LEFT = False
OVERFLOW_RIGHT = True

def printCentered(t, x, y):
    jngl.print(t, int(x-jngl.getTextWidth(t) / 2), y)
root = tkinter.Tk()
root.withdraw()
game = Game()
text = "loading graphics "
dirList = os.listdir("img/World/")
for f in dirList:
    if not f.endswith(".png"):
        continue
    jngl.load("img/World/" + f)
    jngl.print(text, 30, 30)
    text += "."
    jngl.swapBuffers()
    jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
dirList = os.listdir("img/Somyeols")
for f in dirList:
    if not f.endswith(".png"):
        continue
    jngl.load("img/Somyeols/" + f)
    jngl.print(text, 30, 30)
    text += "."
    jngl.swapBuffers()
    jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
dirList = os.listdir("img/gadgets")
for f in dirList:
    if not f.endswith(".png"):
        continue
    jngl.load("img/gadgets/" + f)
    jngl.print(text, 30, 30)
    text += "."
    jngl.swapBuffers()
    jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
text += "\nloading sounds "
dirList = os.listdir("sound/")
for f in dirList:
    if not f.endswith(".ogg"):
        continue
    jngl.load("sound/" + f)
    jngl.print(text, 30, 30)
    text += "."
    jngl.swapBuffers()
    jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)

#load only subdirectorys
levels = []
for f in os.listdir("data/maps/"):
    pass
    if os.path.isdir("data/maps/" + f):
        levels.append(f)
level = 0
start = True
jngl.setBackgroundColor(jngl.Color(0, 0, 0))
running = True
levelselect = False
while running:#not jngl.keyPressed(jngl.key.Escape):

    jngl.swapBuffers()
    jngl.updateInput()
    jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
    while (not jngl.keyPressed(jngl.key.Return) or jngl.keyPressed(jngl.key.Escape)) and not levelselect:
        jngl.draw("img/World/splash.png", (game.windowWidth/2)-jngl.getWidth("img/World/splash.png")/2, (game.windowHeight/2)-jngl.getHeight("img/World/splash.png")/2)
        if jngl.keyPressed(jngl.key.Right):
            level += 1
            if level >= len(levels): level = 0
        elif jngl.keyPressed(jngl.key.Left):
            level -= 1
            if level < 0: level = len(levels)-1
        elif jngl.keyPressed(jngl.key.Escape):
            #import sys
            #jngl.hideWindow()
            running = False
            break
            #sys.exit()
        bouncingEnterButton((game.windowWidth/2) + 320, (game.windowHeight/2)+100)
        bouncingButton((game.windowWidth/2)-225, (game.windowHeight/2) + 115, "img/World/key_left_64.png")
        bouncingButton((game.windowWidth/2)+180, (game.windowHeight/2) + 115, "img/World/key_right_64.png")
        jngl.setFontSize(20)
        jngl.print(levels[level], int((game.windowWidth/2) - jngl.getTextWidth(levels[level]) / 2), (game.windowHeight/2)+138)
        jngl.print("Press F1 for Help", 10, game.windowHeight-30)
        if jngl.keyDown(jngl.key.F1):
            jngl.draw(HELPSCREEN, (game.windowWidth/2)-jngl.getWidth(HELPSCREEN)/2, (game.windowHeight/2)-jngl.getHeight(HELPSCREEN)/2)
        jngl.print("www.somyeol.com", game.windowWidth-180, game.windowHeight-30)
        jngl.swapBuffers()
        jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
        jngl.updateInput()
        selected = 0


    #Level select dialog
    files = os.listdir("data/maps/" + levels[level])
    screen = 0
    screenAnimation = 0
    screenAnimationGoal = screenAnimation
    levellist = []

    counter = 0
    while counter < len(files):
        type = files[counter].split(".")[-1]
        if type == "slv":
            levellist.append(files[counter])
        counter += 1


    jngl.swapBuffers()
    jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)

    lastTime = jngl.getTime()
    needDraw = True
    timePerStep = 0.01
    levelselect = True
    while not jngl.keyPressed(jngl.key.Escape) and not jngl.keyPressed(jngl.key.Return) and running and levelselect:

        if jngl.getTime() - lastTime > timePerStep:
            lastTime += timePerStep
            needDraw = True
            jngl.updateInput()

        elif needDraw:
            overflow = None
            if jngl.keyPressed(jngl.key.Right):
                selected += 1
            elif jngl.keyPressed(jngl.key.Left):
                selected -= 1
            elif jngl.keyPressed(jngl.key.Up):
                selected -= 3
            elif jngl.keyPressed(jngl.key.Down):
                selected += 3

            if selected < 0:
                if len(levellist) == 6:
                    selected = 5
                else:
                    overflow = OVERFLOW_LEFT
            if selected >= len(levellist):
                if len(levellist) == 6:
                    selected = 0
                else:
                    overflow = OVERFLOW_RIGHT

            jngl.draw("img/World/stageselect.png", (game.windowWidth/2)-jngl.getWidth("img/World/stageselect.png")/2, (game.windowHeight/2)-jngl.getHeight("img/World/stageselect.png")/2)
            if screenAnimation != screenAnimationGoal:
                if screenAnimation > screenAnimationGoal:
                    screenAnimation -= 25
                if screenAnimation < screenAnimationGoal:
                    screenAnimation += 25

            if overflow == OVERFLOW_RIGHT:
                screenAnimationGoal = (-1400*((len(levellist)/6)+2))
                if screenAnimation == screenAnimationGoal:
                    screenAnimation = 0
                    selected = 0
                    screen += 1
                    overflow = None

            elif overflow == OVERFLOW_LEFT:
                screenAnimationGoal = 0
                if screenAnimation == screenAnimationGoal:
                    screenAnimation = (-1400*((len(levellist)/6)+1))-500
                    selected = len(levellist)-1
                    screen -= 1
                    overflow = None

            elif overflow == None:
                if selected > (screen * 6) -1:
                    screen += 1
                    screenAnimationGoal -= 1410
                elif selected < (screen * 6) - 6:
                    screen -= 1
                    screenAnimationGoal += 1410

            row = False
            offset =  -(300 * 3)/2 +50
            for i in range(len(levellist)):
                if i % 6 == 0:
                    offset += 130 * 3
                if i % 3 == 0:
                    row = not row
                if row:
                    canvas_preview(((game.windowWidth/2)-500) + (screenAnimation + 1450 + 300*i -offset), (game.windowHeight/2)-100 , i == selected, i, False, levels[level])
                else:
                    canvas_preview(((game.windowWidth/2)-500) + (screenAnimation + 1450 + 300*(i-3) -offset), (game.windowHeight/2)+100 , i == selected, i, False, levels[level])
            jngl.setFontSize(20)
            jngl.print("Press F1 for Help", 10, game.windowHeight-30)
            if jngl.keyDown(jngl.key.F1):
                jngl.draw(HELPSCREEN, (game.windowWidth/2)-jngl.getWidth(HELPSCREEN)/2, (game.windowHeight/2)-jngl.getHeight(HELPSCREEN)/2)        #jngl.print(levels[level], int(445 - jngl.getTextWidth(levels[level]) / 2), 485)
            jngl.print("www.somyeol.com", game.windowWidth-180, game.windowHeight-30)
            jngl.swapBuffers()
            jngl.translate(-jngl.getScreenWidth()/2, -jngl.getScreenHeight()/2)
            #jngl.draw("img/World/canvas.png", self.windowWidth/2 - 137, self.windowHeight/2 - 92)
            jngl.setFontSize(50)
            needDraw = False
        else:
            jngl.sleep(1)
    levelselect = False
    if jngl.keyPressed(jngl.key.Return) and running:
        jngl.setBackgroundColor(jngl.Color(144, 187, 227))
        game.running = True
        game.levelpack = "{0}/".format(levels[level])
        game.levelNr = selected
        game.loadNextLevel()
##        cProfile.run("game.run()")
        game.run()
        game.sound.stopSounds()
        jngl.setBackgroundColor(jngl.Color(0, 0, 0))
        selected = 0
        if not game.levelpack_finished:
            levelselect=True
            selected = game.levelNr-1
    jngl.sleep(100)
    #print levelselect
jngl.hideWindow()
