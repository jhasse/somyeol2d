from Game import *


class Benchmark(Game):
    def newSomyeol(self):
        s = Somyeol.Somyeol(0,0)
        s.initGame(self)
        return s
    def newBox(self):
        b = GameObjects.Box(-100,300,500,32)
        b.initGame(self)
        return b
    def newLock(self):
        l = GameObjects.Lock(0,200)
        l.initGame(self)
        return l
    def run(self):
        lfps = 0
        colsps = 0
        self.level = map.Map()
        self.level.game = self
        self.level.somyeols = [self.newSomyeol()]
        lastTime = jngl.Time()
        self.finish = False
        needDraw = True
        timePerStep = 0.01
        counter = 0
        fps = 0
        start_time = time.time()
        seconds = 0
        end = 0
        min_fps_count = MIN_FPS
        self.moveCamera()
        #self.level.objects.append(self.newBox())
        for i in xrange(10):
            self.level.objects.append(self.newLock())
        lag = True
        while self.running:
            if min_fps_count and jngl.Time() - lastTime > timePerStep:
                lastTime += timePerStep
                needDraw = True
                if jngl.KeyPressed(jngl.key.Escape):
                    self.sound.stopSounds()
                    self.running = False
                if jngl.KeyPressed("s"):
                    self.level.somyeols.append(self.newSomyeol())
                if jngl.KeyPressed("l"):
                    self.level.objects.append(self.newLock())
                if jngl.KeyPressed("r"):
                    self.level.somyeols = [self.newSomyeol()]
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
                #if not min_fps_count and not lag:
                #    self.finish = True
                #else:
                #    lag = False
                min_fps_count = MIN_FPS
                self.sound.playSounds()
                self.checkMusic()
                jngl.SetFontSize(20)
                needDraw = False

                self.level.drawBackground(self.cameray)
                jngl.PushMatrix()
                jngl.Translate(self.windowWidth/2, self.windowHeight)
                jngl.Scale(1 + (self.scale - 1) / 2)
                jngl.Translate(self.camerax / 2, -self.windowHeight + self.cameray / 2)
                for i in range(-2, 3):
                    jngl.Draw(RESOURCEWORLD + "mountains.png", i*1024, self.windowHeight-300)
                jngl.PopMatrix()
                jngl.PushMatrix()
                jngl.Scale(self.scale)
                jngl.Translate(self.camerax, self.cameray)
                self.level.draw()
                #uncomment for visualization of boundingbox                
                #jngl.SetColor(255,0,0,150)
                #jngl.DrawRect(self.bounds.x,self.bounds.y,self.bounds.width,self.bounds.height)  
                jngl.PopMatrix()

                jngl.SetSpriteColor(255, 255, 255, 150)
                jngl.Draw("img/World/canvas.png", -80, -100)
                jngl.Print("Somyeols: {0}".format(len(self.level.somyeols)), 10, 10)
                jngl.Draw("img/World/canvas.png", self.windowWidth - 200, -120)
                jngl.Print("Level: {0}".format(self.levelNr), self.windowWidth - 140, 10)
                jngl.SetSpriteColor(255, 255, 255)
                
                jngl.Print("Time: %.2f"%(seconds), 10, 40)

                if self.finish:
                    x,y = (self.windowWidth/2) - (jngl.GetWidth("img/World/canvas.png")/2), (self.windowHeight/2) - (jngl.GetHeight("img/World/canvas.png")/2)
                    jngl.Draw("img/World/canvas.png", self.windowWidth/2 - 137, self.windowHeight/2 - 92)
                    jngl.Print("Score", x+(jngl.GetWidth("img/World/canvas.png")/2), y+20)
                    jngl.SetFontSize(50)
                    jngl.Print(str(colsps), x+10, y+70)
                    bouncingEnterButton(x+50, y+jngl.GetHeight("img/World/canvas.png")+50)
                    if jngl.KeyPressed(jngl.key.Return):
                        self.running=False
                    jngl.SwapBuffers()
                    continue
                else:
                    seconds = time.time()-start_time

                fps += jngl.FPS() / 50
                counter -= 1
                if counter < 0:
                    counter = 50
                    jngl.SetTitle("Somyeol2D {0} - FPS: {1}".format(self.version, int(fps)))
                    lfps = fps
                    if lfps > 60:
                        self.level.somyeols.append(self.newSomyeol())
                        colsps = len(self.level.objects)*len(self.level.somyeols)*100*2
                        end = 0
                    else:
                        end+=1
                        if end == 20:
                            self.finish = True
                    fps = 0
                jngl.SetFontSize(20)  
                jngl.Print("FPS {0}".format(lfps), self.windowWidth-180, self.windowHeight-30)  
                jngl.Print("Objects {0} Somyeol {1} Score {2}".format(len(self.level.objects),len(self.level.somyeols),colsps), 10, self.windowHeight-30)  
                if jngl.KeyDown(jngl.key.F1):
                    jngl.Draw(HELPSCREEN, (self.windowWidth/2)-jngl.GetWidth(HELPSCREEN)/2, (self.windowHeight/2)-jngl.GetHeight(HELPSCREEN)/2)
                
                #uncomment for visualization of collision-count
                #colcount = 0
                #for o in self.level.objects:
                #    if o.canCollide:
                #        colcount+=1
                #jngl.Print(str(colcount), self.windowWidth-680, self.windowHeight-50)     
                            
                jngl.SwapBuffers()
            else:
                jngl.Sleep(1)
            min_fps_count-=1
        self.sound.stopSounds()
benchmark = Benchmark()
benchmark.run()