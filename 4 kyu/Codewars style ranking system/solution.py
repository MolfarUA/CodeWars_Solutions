class User:
    RANKS = (-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8)
    i = 0
    rank = RANKS[i]
    progress = 0
         
    def inc_progress(self, activity):
        if activity not in self.RANKS:
            raise ValueError
        
        delta = self.RANKS.index(activity) - self.RANKS.index(self.rank)
        if delta == 0:
            self.progress += 3
        elif delta == -1:
            self.progress += 1
        elif delta > 0:
            self.progress += delta * delta * 10
                    
        while self.progress >= 100 and self.i < 15:
            self.i += 1
            self.progress -= 100
            self.rank = self.RANKS[self.i]
            
        if self.i == 15:
            self.progress = 0
_____________________________________
class User ():    
    def __init__ (self):
        self.RANKS = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]
        self.rank = -8
        self.rank_index = 0
        self.progress = 0
        
    def inc_progress (self, rank):
        rank_index = self.RANKS.index(rank)
        
        if rank_index == self.rank_index:
            self.progress += 3
        elif rank_index == self.rank_index - 1:
            self.progress += 1
        elif rank_index > self.rank_index:
            difference = rank_index - self.rank_index
            self.progress += 10 * difference * difference
            
        while self.progress >= 100:
            self.rank_index += 1
            self.rank = self.RANKS[self.rank_index]
            self.progress -= 100    
        
        if self.rank == 8:
            self.progress = 0
            return
_____________________________________
class User(object):
  def __init__(self):
    self.ranks, self.cur_rank, self.progress = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8], 0, 0
  def get_rank(self):
    return self.ranks[self.cur_rank]
  def set_rank(self, arg):
    '''Nope'''
  rank = property(get_rank, set_rank)
  def inc_progress(self, k_rank):
    k_rank = self.ranks.index(k_rank)
    if self.rank == 8: return
    if k_rank == self.cur_rank: self.progress += 3
    elif k_rank == self.cur_rank - 1: self.progress += 1
    elif k_rank > self.cur_rank:
      diff = k_rank - self.cur_rank
      self.progress += 10 * diff * diff
    while self.progress >= 100:
      self.cur_rank += 1
      self.progress -= 100
      if self.rank == 8:
        self.progress = 0
        return
_____________________________________
class User:

    def __init__(self):
        self.rank = -8
        self.progress = 0

    def inc_progress(self, act):
        assert act in range(-8, 0) + range(1, 9)
        diff = act - (act > 0) - self.rank + (self.rank > 0)
        self.progress += (0, 1, 3, diff * diff * 10)[(diff > 0) + (diff >= 0) + (diff >= -1)]
        while self.progress >= 100:
            self.rank += 1 + (self.rank == -1)
            self.progress -= 100
        if self.rank >= 8:
            self.rank, self.progress = 8, 0
_____________________________________
class User:
    Ranks = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]
    
    def __init__(self):
        self.__rank = -8
        self.__progress = 0
    
    @property
    def rank(self):
        return self.__rank
    
    @property
    def progress(self):
        return self.__progress
    
    def inc_progress(self, kata_rank):
        self.__validate_rank(kata_rank)
        progress_made = self.__calc_progress(kata_rank) 
        new_progress = self.progress + progress_made
        extra_rank, progress_left = self.__calc_rank(new_progress)
        self.__update_rank(extra_rank)
        self.__update_progress(progress_left)
        
    def __validate_rank(self, in_rank):
        if (in_rank not in self.Ranks):
            raise ValueError("Rank must be in range [-8,-1]U[1,8]")
        
    def __calc_progress(self, kata_rank):
        diff = self.Ranks.index(kata_rank) - self.Ranks.index(self.rank)
        if (kata_rank > self.rank):
            return 10 * diff ** 2
        elif (kata_rank == self.rank):
            return 3
        elif (diff == - 1):
            return 1
        else:
            return 0

    def __calc_rank(self, new_progress):
        extra_rank = 0
        progress_left = new_progress
        if (new_progress > 99 and self.rank < 8):
            extra_rank = new_progress // 100
            progress_left = new_progress % 100
        return extra_rank, progress_left
    
    def __update_progress(self, new_progress):
        self.__progress = new_progress
        if (self.rank == 8 and self.progress>0):
            self.__progress = 0
    
    def __update_rank(self, extra_rank):
        new_rank = self.rank + extra_rank
        if (self.rank < 0 and new_rank >= 0):
            new_rank = new_rank + 1
        if (new_rank > 8):
            self.__rank = 8
        else:
            self.__rank = new_rank            
_____________________________________
class User(object):
    
    MAX_RANK, MAX_PROGRESS, DELTA_RANKS = 8, 100, set(range(-8,9))-{0}
    
    def __init__(self):
        self.rank, self.progress = -8, 0
    
    def inc_progress(self, rank):
        if not rank in self.DELTA_RANKS:
            raise ValueError("Invalid value for activity rank")
        dRank = rank - self.rank + (rank * self.rank < 0) * (-1)**(rank > self.rank)
        self.updateProgress([0, 1, 3, 10 * dRank**2][ (dRank > -2) + (dRank >= 0) + (dRank > 0)] )
        
    def updateProgress(self,n):
        nLevel, self.progress = divmod(self.progress + n, self.MAX_PROGRESS)
        self.rank = min(self.MAX_RANK, self.rank + nLevel + (self.rank+nLevel not in self.DELTA_RANKS))
        if self.rank == self.MAX_RANK: self.progress = 0
_____________________________________
class User:
    ranks = range(-8,0) + range(1,9)

    def __init__(self):
        self.rank = -8
        self.progress = 0
        
    def inc_progress(self, rank):
        if rank not in User.ranks :
            raise ValueError('Invalid rank')
        d = User.ranks.index(rank) - User.ranks.index(self.rank)
        p = 0 if d  < -1 else (
            1 if d == -1 else (
            3 if d ==  0 else 10 * d * d ))
        r = int( (self.progress + p) / 100 )
        r = User.ranks.index(self.rank) + r
        self.rank = User.ranks[r if r < len(User.ranks) else -1]
        self.progress = (self.progress + p) % (100 if self.rank < User.ranks[-1] else 1)
_____________________________________
class User:
    rank = -8
    progress = 0

    def inc_progress(self, rank):
        if rank < -8 or rank == 0 or 8 < rank:
            raise
        diff = rank - (rank > 0) - self.rank + (self.rank > 0)
        if diff < -1:
            return
        self.progress += {-1: 1, 0: 3}.get(diff, 10 * diff ** 2)
        while self.progress >= 100 and self.rank < 8:
            self.progress -= 100
            self.rank += 1 + (self.rank == -1)

        if self.rank == 8:
            self.progress = 0
_____________________________________
class User():
    '''Creates a User class for a codewars style website'''

    def __init__(self):
        self.ranks = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]    #15
        self.progress = 0
        self.level = 0
        self.rank = self.ranks[self.level]

    def inc_progress(self, rank):

        if rank not in self.ranks:
            raise Exception('Invalid rank')
        
        activityrank = self.ranks.index(rank)
        rank = self.level
        difference = activityrank - rank

        if self.level < 15:

            if difference > 0:                                              
                points = 10 * difference * difference
                self.progress += points

            elif difference == 0: self.progress += 3

            elif difference == -1: self.progress += 1 
            
            if self.progress == 100:
                self.level += 1 
                self.rank = self.ranks[self.level]
                self.progress = 0

            while self.progress >= 100:
                self.level += 1
                leftover = self.progress - 100
                self.rank = self.ranks[self.level]

                if self.level < 15:
                    self.progress = leftover

                elif self.level >= 15:
                    self.progress = 0
_____________________________________
class User:
    def get_rank(self):
        if self._rank < 0:
            return self._rank
        else:
            return self._rank + 1
    
    progress = 0
    _rank = -8
    rank = property(get_rank)
        
    def check_progress(self):
        self._rank += self.progress // 100
        self.progress %= 100
        if self._rank > 6:
            self.progress = 0
            self._rank = 7
        
    def inc_progress(self, act_rank):
        if act_rank == 0 or act_rank > 8 or act_rank < -8:
            raise ValueError
        if act_rank > 0:
            act_rank -= 1
        
        delta = act_rank - self._rank
        if delta == 0:
            self.progress += 3
        elif delta == -1:
            self.progress += 1
        elif delta > 0:
            self.progress += (delta ** 2) *  10
        self.check_progress()
_____________________________________
class User():
    def __init__(self):
        self._kyudan = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]
        self._max_rank = len(self._kyudan) - 1
        self._rank = 0
        self.progress = 0
            
    @property
    def rank(self):
        return self._kyudan[self._rank]
    
    def _kyudan_to_rank(self, kd):
        return self._kyudan.index(kd)

    def inc_progress(self, pg):
        # will raise an error if pg not in _kyudan
        d = self._kyudan_to_rank(pg) - self._rank 
        
        if self._rank != self._max_rank:
            if d > 0:
                self.progress += 10 * d ** 2
            elif d == 0:
                self.progress += 3
            elif d == -1:
                self.progress += 1

            while self.progress >= 100:
                self.progress -= 100
                self._rank += 1
                if self._rank == self._max_rank:
                    self.progress = 0
