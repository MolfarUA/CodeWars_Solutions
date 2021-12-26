class Miner:
    def __init__(self, exp=0):
        self.level = next(i for i in range(40, 0, -1) if exp >= EXPERIENCE[i])
        self.exp = exp
    
    def mine(self, rock):
        lvl, exp = ROCKS[rock]
        if self.level >= lvl:
            self.exp += exp
            if self.level < 40 and self.exp >= EXPERIENCE[self.level+1]:
                self.level += 1
                return f"Congratulations, you just advanced a Mining level! Your mining level is now {self.level}."
            return "You swing your pick at the rock."
        return f"You need a mining level of {lvl} to mine {rock}."
      
########################
from preloaded import EXPERIENCE, ROCKS
from math import inf


class Miner:
    
    LEVELS    = sorted(EXPERIENCE.values()) + [inf]
    ROCKS_LVL = {r:lvl for r,(lvl,_) in ROCKS.items()}
    ROCKS_XP  = {r:xp for r,(_,xp) in ROCKS.items()}
    
    NOPE         = 'You need a mining level of {} to mine {}.'
    LVL_UP       = "Congratulations, you just advanced a Mining level! Your mining level is now {}."
    STILL_MINING = "You swing your pick at the rock."
    
    def __init__(self, xp=0):
        self.xp  = xp
        self.lvl = next(i for i,v in enumerate(self.LEVELS) if v>xp)
    
    def mine(self, rock):
        if self.ROCKS_LVL[rock]>self.lvl:
            return self.NOPE.format(self.ROCKS_LVL[rock], rock)
        self.xp += self.ROCKS_XP[rock]
        lvlUp    = self.xp >= self.LEVELS[self.lvl]
        if lvlUp:
            self.lvl += 1
            return self.LVL_UP.format(self.lvl)
        return self.STILL_MINING
      
#######################
from preloaded import EXPERIENCE, ROCKS
from bisect import bisect_right

class Miner:
    EXPS=list(EXPERIENCE.values())
    
    def __init__(self, xp=0):
        self.xp=xp
        self.l=1
        self.update_level()
    
    def mine(self, rock):
        rl,x=ROCKS[rock]
        if rl>self.l:
            return f"You need a mining level of {rl} to mine {rock}."
        else:
            self.xp+=x
            return self.update_level()
    
    def update_level(self):
        nl=bisect_right(Miner.EXPS,self.xp)
        if nl!=self.l:
            self.l=nl
            return f"Congratulations, you just advanced a Mining level! Your mining level is now {nl}."
        else:
            return "You swing your pick at the rock."
          
##########################
from preloaded import EXPERIENCE, ROCKS

class Miner:
    def __init__(self, xp=0):
        self.xp = xp
        self.level = 0
        for l, xp in EXPERIENCE.items():
            if self.xp >= xp:
                self.level = l
            else:
                break
    
    def mine(self, rock):
        l, xp = ROCKS[rock]
        if l > self.level:
            return f"You need a mining level of {l} to mine {rock}."
        else:
            self.xp += xp
            if self.level < 40 and EXPERIENCE[self.level+1] <= self.xp:
                self.level += 1
                return f'Congratulations, you just advanced a Mining level! Your mining level is now {self.level}.'
            return "You swing your pick at the rock."
          
#########################
from preloaded import EXPERIENCE, ROCKS

class Miner:
    def __init__(self, xp=0):
        self.xp = xp
        self.level = None

    def get_lvl(self):
        for lvl, lvl_xp in EXPERIENCE.items():
            if self.xp >= lvl_xp:
                self.level = lvl
        return self.level

    def mine(self, rock):
        start_lvl = self.get_lvl()
        if ROCKS[rock][0] <= start_lvl:
            self.xp += ROCKS[rock][1]
        else:
            return f"You need a mining level of {ROCKS[rock][0]} to mine {rock}."
        if start_lvl < self.get_lvl():
            return f"Congratulations, you just advanced a Mining level! Your mining level is now {self.get_lvl()}."
        return "You swing your pick at the rock."
      
#####################
from preloaded import EXPERIENCE, ROCKS
MAX_LEVEL = len(EXPERIENCE)


class Miner:
    def __init__(self, xp=0):
        self.xp = xp
        self.level = self.xp_to_level()
    
    def mine(self, rock):
        level, xp = ROCKS[rock]
        if self.level >= level:
            self.xp += xp
            return self.update_level()
        else:
            return f"You need a mining level of {level} to mine {rock}."
    
    def update_level(self):
        if self.level < MAX_LEVEL and self.xp >= EXPERIENCE[self.level + 1]:
            self.level += 1
            return f"Congratulations, you just advanced a Mining level! Your mining level is now {self.level}."
        else:
            return "You swing your pick at the rock."
        
    def xp_to_level(self):
        for lvl in range(1, MAX_LEVEL):
            if self.xp >= EXPERIENCE[lvl] and self.xp < EXPERIENCE[lvl + 1]:
                return lvl

        return MAX_LEVEL
      
#####################
from preloaded import EXPERIENCE, ROCKS
from typing import Tuple

class Miner:
    def __init__(self, xp=0):
        self.xp = xp
        self.MAX_LEVEL = 40
    
    def mine(self, rock):
        rock_level_and_exp: Tuple[int, int] = ROCKS[rock]
        
        before_mining_lvl = self._level(self.xp)
        if (before_mining_lvl < rock_level_and_exp[0]):
            return f"You need a mining level of {rock_level_and_exp[0]} to mine {rock}."
        else: 
            self.xp += rock_level_and_exp[1]
            after_mining_lvl = self._level(self.xp)
            if (before_mining_lvl < after_mining_lvl):
                return f"Congratulations, you just advanced a Mining level! Your mining level is now {after_mining_lvl}."
            else: 
                return "You swing your pick at the rock."
            
    def _level(self, exp: int): 
        for i in range(self.MAX_LEVEL, 0, -1):
            if (exp >= EXPERIENCE[i]):
                return i
        
        
############################
from preloaded import EXPERIENCE, ROCKS


class Miner:
    def __init__(self, xp=0):
        self.exp = xp
        for key, value in EXPERIENCE.items():
            if self.exp >= value:
                self.level = key
    
    def mine(self, rock):
        if rock in ROCKS:
            if self.level >= ROCKS[rock][0]:
                self.exp += ROCKS[rock][1]
                lvl = self.level
                for key, value in EXPERIENCE.items():
                    if self.exp >=  value:
                        self.level = key
                if lvl < self.level:
                        return f'Congratulations, you just advanced a Mining level! Your mining level is now {self.level}.'
                elif lvl >= self.level:
                        return 'You swing your pick at the rock.'
            else:
                return f"You need a mining level of {ROCKS[rock][0]} to mine {rock}."
                 
                
#############################
from preloaded import EXPERIENCE, ROCKS

class Miner:
    def __init__(self, xp=0):
        self.__xp = xp

        if self.__xp >= max(EXPERIENCE.values()):
            self.__level = 40
        else:
            prev_lvl = None
            for lvl, exp in EXPERIENCE.items():
                if self.__xp < exp:
                    self.__level = prev_lvl
                    break
                prev_lvl = lvl

    @property
    def level(self):
        if self.__xp >= max(EXPERIENCE.values()):
            return 40
        else:
            prev_lvl = None
            for lvl, exp in EXPERIENCE.items():
                if self.__xp < exp:
                    return prev_lvl
                prev_lvl = lvl

    def mine(self, rock):
        lvl, xp = ROCKS[rock]
        lvl_before_mining = self.level
        if self.level < lvl:
            return f'You need a mining level of {lvl} to mine {rock}.'
        else:
            self.__xp += xp
            if lvl_before_mining != self.level:
                return f'Congratulations, you just advanced a Mining level! Your mining level is now {self.level}.'
            else:
                return f'You swing your pick at the rock.'
