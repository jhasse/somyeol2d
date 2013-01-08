# -*- coding: utf-8 -*-
##############################################################
## 
##############################################################

import pickle
import sys, os

class LevelScore(object):
    '''
    '''
    def __init__(self, score=0, time=0):
        '''
        '''
        self.score = score
        self.time = time
    
    # -------------------------------------------------------------------------
    
    def __lt__(self, other):
        '''
        '''
        return self.rank < other.rank
    
    # -------------------------------------------------------------------------
    
    def __eq__(self, other):
        '''
        '''
        return self.rank == other.rank
    
    # -------------------------------------------------------------------------
    
    def __gt__(self, other):
        '''
        '''
        return self.rank > other.rank
    
    # -------------------------------------------------------------------------

    def __str__(self):
        '''
        '''
        return "score: %d, time: %d, rank: %d" % (self.score, self.time, self.rank)
    
    # -------------------------------------------------------------------------
    
    def __repr__(self):
        '''
        '''
        return "(|%d, %d, %d|)" % (self.score, self.time, self.rank)
    
    # -------------------------------------------------------------------------
    
    def getRank(self):
        '''
        '''
        if self.time == 0:
            return 0
        else:
            return self.score/float(self.time)
    rank = property(getRank)

    # -------------------------------------------------------------------------

# -----------------------------------------------------------------------------7
# -----------------------------------------------------------------------------

class HighScore(object):
    def __init__(self):
        self.scores = []
        self.use_apppath = True
        
    def loadHighscore(self,levelpack):
        self.use_apppath = True
        try:
            if sys.platform == "win32" and self.use_apppath:
                lpackpath = os.environ['APPDATA']+"/somyeol/highscore/{0}".format(levelpack)
            else:
                lpackpath = os.path.expanduser("~/.somyeol/highscore/{0}".format(levelpack))
            if not os.path.exists(lpackpath):
                os.makedirs(lpackpath)
            file = open(lpackpath+"highscore.hsc", "rb")
            data = pickle.load(file, fix_imports=True)
            self.scores = data
        except EOFError:
            jngl.errorMessage("Empty file: {0}".format(path))
        except: return
    
    # -------------------------------------------------------------------------
    
    def newHighscore(self, level, time, score):
        '''
        '''
        rank = score/float(time)            # calculate the new rank

        # if no highscores are available, create them
        while len(self.scores) <= level:
            self.scores.append([])
        new_score = LevelScore(score,time)
        # append the new score
        self.scores[level].append(new_score)
        self.scores[level].sort()       # sort the highscore
        self.scores[level].reverse()    # the biggest value is at the start position
        while len(self.scores[level]) > 5: # cut off the smallest values
            self.scores[level].pop()

        # return true, if the rank was a new highscore
        if self.scores[level][-1].rank <= rank:
            return new_score
        else:
            return False
    
    # -------------------------------------------------------------------------
        
    def saveHighscore(self,levelpack):
        '''
        '''
        if sys.platform == "win32" and self.use_apppath:
            lpackpath = os.environ['APPDATA']+"/somyeol/highscore/{0}".format(levelpack)
        else:
            lpackpath = os.path.expanduser("~/.somyeol/highscore/{0}".format(levelpack))
        if not os.path.exists(lpackpath):
            os.makedirs(lpackpath)
        file = open(lpackpath+"highscore.hsc", "wb")
        data = self.scores
        pickle.dump(data, file)
    
    # -------------------------------------------------------------------------
    
    def getLevelScore(self, level):
        '''
        '''
        output = []
        if level < len(self.scores):
            output = self.scores[level]
        
        while len(output) < 5:
            output.append(LevelScore(0,0))
        
        return output
    
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    
if __name__ == '__main__':
    import main
