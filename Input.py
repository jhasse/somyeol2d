# -*- coding: utf-8 -*-
##############################################################
## 
##############################################################

class Input(object):
    def __init__(self):
        if jngl.keyDown(jngl.key.Right):
            self.xspeed += 0.2
        if jngl.keyDown(jngl.key.Left):
            self.xspeed -= 0.2
            
        
if __name__ == "__main__":
    import main
