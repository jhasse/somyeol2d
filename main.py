# -*- coding: utf-8 -*-
##############################################################
##
##############################################################
import jngl
import os
from tkFileDialog import *
import Tkinter
##import cProfile
from Game import Game, bouncingEnterButton, bouncingButton, canvas_preview
HELPSCREEN = "img/World/helpscreen.png"

OVERFLOW_LEFT = False
OVERFLOW_RIGHT = True

def printCentered(t, x, y):
    jngl.Print(t, int(x-jngl.GetTextWidth(t) / 2), y)
root = Tkinter.Tk()
root.withdraw()
game = Game()
if not jngl.IsOpenALInstalled():
    jngl.Print("Installing OpenAl... Please be patient...", 30, 30)
    jngl.SwapBuffers()
    os.system("oalinst.exe -s")
text = "loading graphics "
dirList = os.listdir("img/World/")
for f in dirList:
    if not f.endswith(".png"):
        continue
    jngl.Load("img/World/" + f)
    jngl.Print(text, 30, 30)
    text += "."
    jngl.SwapBuffers()
dirList = os.listdir("img/Somyeols")
for f in dirList:
    if not f.endswith(".png"):
        continue
    jngl.Load("img/Somyeols/" + f)
    jngl.Print(text, 30, 30)
    text += "."
    jngl.SwapBuffers()
dirList = os.listdir("img/gadgets")
for f in dirList:
    if not f.endswith(".png"):
        continue
    jngl.Load("img/gadgets/" + f)
    jngl.Print(text, 30, 30)
    text += "."
    jngl.SwapBuffers()
text += "\nloading sounds "
dirList = os.listdir("sound/")
for f in dirList:
    if not f.endswith(".ogg"):
        continue
    jngl.Load("sound/" + f)
    jngl.Print(text, 30, 30)
    text += "."
    jngl.SwapBuffers()

#load only subdirectorys
levels = []
for f in os.listdir("data/maps/"):
    pass
    if os.path.isdir("data/maps/" + f):
        levels.append(f)
level = 0
start = True
jngl.SetBackgroundColor(0,0,0)
running = True
levelselect = False
while running:#not jngl.KeyPressed(jngl.key.Escape):

    jngl.SwapBuffers()
    while (not jngl.KeyPressed(jngl.key.Return) or jngl.KeyPressed(jngl.key.Escape)) and not levelselect:
        jngl.Draw("img/World/splash.png", (game.windowWidth/2)-jngl.GetWidth("img/World/splash.png")/2, (game.windowHeight/2)-jngl.GetHeight("img/World/splash.png")/2)
        if jngl.KeyPressed(jngl.key.Right):
            level += 1
            if level >= len(levels): level = 0
        elif jngl.KeyPressed(jngl.key.Left):
            level -= 1
            if level < 0: level = len(levels)-1
        elif jngl.KeyPressed(jngl.key.Escape):
            #import sys
            #jngl.HideWindow()
            running = False
            break
            #sys.exit()
        bouncingEnterButton((game.windowWidth/2) + 320, (game.windowHeight/2)+100)
        bouncingButton((game.windowWidth/2)-225, (game.windowHeight/2) + 115, "img/World/key_left_64.png")
        bouncingButton((game.windowWidth/2)+180, (game.windowHeight/2) + 115, "img/World/key_right_64.png")
        jngl.SetFontSize(20)
        jngl.Print(levels[level], int((game.windowWidth/2) - jngl.GetTextWidth(levels[level]) / 2), (game.windowHeight/2)+138)
        jngl.Print("Press F1 for Help", 10, game.windowHeight-30)
        if jngl.KeyDown(jngl.key.F1):
            jngl.Draw(HELPSCREEN, (game.windowWidth/2)-jngl.GetWidth(HELPSCREEN)/2, (game.windowHeight/2)-jngl.GetHeight(HELPSCREEN)/2)
        jngl.Print("www.somyeol.com", game.windowWidth-180, game.windowHeight-30)
        jngl.SwapBuffers()
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


    jngl.SwapBuffers()

    lastTime = jngl.Time()
    needDraw = True
    timePerStep = 0.01
    levelselect = True
    while not jngl.KeyPressed(jngl.key.Escape) and not jngl.KeyPressed(jngl.key.Return) and running and levelselect:

        if jngl.Time() - lastTime > timePerStep:
            lastTime += timePerStep
            needDraw = True

        elif needDraw:
            overflow = None
            if jngl.KeyPressed(jngl.key.Right):
                selected += 1
            elif jngl.KeyPressed(jngl.key.Left):
                selected -= 1
            elif jngl.KeyPressed(jngl.key.Up):
                selected -= 3
            elif jngl.KeyPressed(jngl.key.Down):
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

            jngl.Draw("img/World/stageselect.png", (game.windowWidth/2)-jngl.GetWidth("img/World/stageselect.png")/2, (game.windowHeight/2)-jngl.GetHeight("img/World/stageselect.png")/2)
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
            jngl.SetFontSize(20)
            jngl.Print("Press F1 for Help", 10, game.windowHeight-30)
            if jngl.KeyDown(jngl.key.F1):
                jngl.Draw(HELPSCREEN, (game.windowWidth/2)-jngl.GetWidth(HELPSCREEN)/2, (game.windowHeight/2)-jngl.GetHeight(HELPSCREEN)/2)        #jngl.Print(levels[level], int(445 - jngl.GetTextWidth(levels[level]) / 2), 485)
            jngl.Print("www.somyeol.com", game.windowWidth-180, game.windowHeight-30)
            jngl.SwapBuffers()
            #jngl.Draw("img/World/canvas.png", self.windowWidth/2 - 137, self.windowHeight/2 - 92)
            jngl.SetFontSize(50)
            needDraw = False
        else:
            jngl.Sleep(1)
    levelselect = False
    if jngl.KeyPressed(jngl.key.Return) and running:
        jngl.SetBackgroundColor(144, 187, 227)
        game.running = True
        game.levelpack = "{0}/".format(levels[level])
        game.levelNr = selected
        game.loadNextLevel()
##        cProfile.run("game.run()")
        game.run()
        game.sound.stopSounds()
        jngl.SetBackgroundColor(0,0,0)
        selected = 0
        if not game.levelpack_finished:
            levelselect=True
            selected = game.levelNr-1
    jngl.Sleep(100)
    #print levelselect
jngl.HideWindow()
