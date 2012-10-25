import jngl

class Image(object):
    def __init__(self, x, y, filename):
        self.x = x
        self.y = y
        self.filename = filename
        self.width = jngl.getWidth(filename)
        self.height = jngl.getHeight(filename)
    def draw(self):
        jngl.draw(self.filename, self.x, self.y)
    def checkCollision(self, other):
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

if __name__ == '__main__':
    import main
