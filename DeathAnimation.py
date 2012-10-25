import jngl
from Somyeol import RESOURCE

class DeathAnimation:
    def __init__(self, x, y):
        self.filenames = [RESOURCE+"dead_0.png", RESOURCE+"dead_1.png", RESOURCE+"dead_2.png"]
        self.i = 0
        self.x = x
        self.y = y
        self.cnt = 10
    def step(self, animations):
        self.cnt -= 1
        if self.cnt < 0:
            self.cnt = 10
            self.i += 1
            if self.i >= len(self.filenames):
                animations.remove(self)
    def draw(self):
        jngl.Draw(self.filenames[self.i], self.x-jngl.GetWidth(self.filenames[self.i])/2, self.y-jngl.GetHeight(self.filenames[self.i])/2)