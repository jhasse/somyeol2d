# -*- coding: utf-8 -*-
import jngl
import Somyeol
import random
import os

SOUND = "sound/"
class Sound(object):
    def __init__(self, game):
        self.game = game
        self.sound_queue = set()
        self.somyeol_count = 0
        self.walk_sounds_playing = 0
        self.sound_walk = False
        self.sounds_playing = 0
        self.sound_land = 0
        self.playing_sounds = []
        jngl.SetVolume(50)

        #Generate a list of all sound-files
        self.sounds = []
        dirList = os.listdir(SOUND)
        for f in dirList:
            if not f.endswith(".ogg"):
                continue
            self.sounds.append(SOUND+f)
    def stopSounds(self):
        for sound in self.sounds:
            jngl.Stop(sound)
    def updateSoundsPlaying(self):
        self.sounds_playing = 0
        self.walk_sounds_playing = 0
        self.playing_sounds = []
        for sound in self.sounds:
            if jngl.IsPlaying(sound):
                self.playing_sounds.append(sound)
                if sound in Somyeol.Somyeol.sound_walk:
                    self.walk_sounds_playing += 1
                else:
                    self.sounds_playing +=1

    def playSounds(self):

        self.somyeol_count = len(self.game.level.somyeols)
        self.updateSoundsPlaying()

        #Sounds that are used by alot of Somyeols get a special treatment (walking and jumping)

        if jngl.KeyDown(jngl.key.Up):
            #Stop other sounds if jumping
            for sound in Somyeol.Somyeol.sound_walk:
                jngl.Stop(sound)
            for sound in Somyeol.Somyeol.sound_walk_crowd:
                jngl.Stop(sound)

        #play other sounds...
        for sound in self.sound_queue:
            if sound in Somyeol.Somyeol.sound_walk:
                if self.walk_sounds_playing >= self.somyeol_count:
                    continue
            else:
                if self.sounds_playing >= self.somyeol_count:
                    continue
            if not sound in self.playing_sounds:
                jngl.Play(sound)
            else:
                #use the crowd sounds
                if sound in Somyeol.Somyeol.sound_jump:
                    sound = Somyeol.Somyeol.sound_jump_crowd[random.randint(0,len(Somyeol.Somyeol.sound_jump_crowd)-1)]
                    if not jngl.IsPlaying(sound):
                        jngl.Play(sound)
                elif sound in Somyeol.Somyeol.sound_walk:
                    sound = Somyeol.Somyeol.sound_walk_crowd[random.randint(0,len(Somyeol.Somyeol.sound_walk_crowd)-1)]
                    if not jngl.IsPlaying(sound):
                        jngl.Play(sound)
        self.sound_queue.clear()

    def getSound(self, list):
        return list[random.randint(0,len(list))-1]

    def addToQueue(self, sound):
        if sound in Somyeol.Somyeol.sound_walk:
            if self.walk_sounds_playing >= self.somyeol_count:
                return
        self.sound_queue.add(sound)
if __name__ == "__main__":
    import main
