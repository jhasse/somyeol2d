#import pyximport; pyximport.install()
#import collision
try:
    import collision
    use_c = True
except:
    use_c = False
    
class Collidable(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        
class GameObject(object):
    def __init__(self):
        self.canCollide = False
    def checkCollision(self, other):
        if use_c:
            return collision.c_checkCollision(self.x,self.y,other.x,other.y,self.width,self.height,other.width,other.height)
        left1 = self.x
        left2 = other.x
        right1 = self.x + self.width
        right2 = other.x + other.width
        top1 = self.y
        top2 = other.y
        bottom1 = self.y + self.height
        bottom2 = other.y + other.height

        if left1 > right2:
            return False
        if left2 > right1:
            return False
        if top1 > bottom2:
            return False
        if top2 > bottom1:
            return False
        return True
    def isBox(self):
        return False
    def initGame(self, game):
        self.canCollide = False
        self.game = game
    def handleCollision(self, other):
        pass
    def step(self):
        pass
    def __str__(self):
        return self.__class__.__name__
    def draw(self):
        pass
    def drawEditor(self):
        self.draw()

if __name__ == '__main__':
    import main

