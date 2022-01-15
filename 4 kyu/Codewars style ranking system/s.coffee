class User
  ranks = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]

  constructor: ->
    @rank = -8
    @progress = 0
    
  incProgress: (rank) ->
    throw new OutOfRangeException if (ranks.indexOf rank) == -1
    
    if @rank != 8
      delta = (ranks.indexOf rank) - ranks.indexOf @rank
      
      if delta > -2
        @progress = @progress +
          switch delta
            when -1 then 1
            when  0 then 3
            else 10 * delta * delta
          
      if @progress >= 100
        @rank = ranks[(ranks.indexOf @rank) + (Math.floor @progress / 100)]
        @progress = @rank != 8 && @progress % 100 || 0
_____________________________________
class User
  constructor: ->
    @rank = -8
    @progress = 0
  
  incProgress: (target) ->
    throw new Error() unless Math.abs(target) in [1,2,3,4,5,6,7,8]
    
    r = if @rank < 0 then @rank else @rank-1
    t = if target < 0 then target else target-1
    if t-r > 0
      p =  (t - r)**2*10 + @progress
    else if t-r is 0
      p = 3 + @progress
    else if t-r > -2
      p = 1 + @progress
    else
      p = @progress
    if p > (7 - r)*100
      @rank = 8
      @progress = 0
    else
      @rank += p/100 | 0
      @rank = if @rank then @rank else 1
      @progress = p%100
_____________________________________
Function::property = (prop, desc) ->
  Object.defineProperty @prototype, prop, desc
  
class User
  
  constructor: () ->
    @r = 0
    @p = 0
    @ranks = [-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8]
  
  @property 'rank',
    get: -> @ranks[@r]
    set: (value) -> @r = @ranks.indexOf(value)
    
  @property 'progress',
    get: -> @p
    set: (value) -> @p = value
    
  incProgress: (rank) ->
    rank = @ranks.indexOf(rank)
    if rank == -1
      throw 'error'
    if rank < @r - 1
      return
    if rank == @r
      @p += 3
    else if rank == @r - 1
      @p += 1
    else
      @p += (@r - rank) ** 2 * 10
    while @p >= 100
      @r++
      @p -= 100
    if @r >= @ranks.length - 1
      @p = 0
    @r = Math.min(@r, @ranks.length - 1)
_____________________________________
class User
  constructor: ->
    @rank = -8
    @progress = 0
  incProgress: (pro)->
    if not (9 > pro > -9) or pro is 0
      throw "erro"
    else
      if pro > 0 and @rank < 0 then pro -= 1
      if pro < 0 and @rank > 0 then pro += 1
    @progress += switch
      when pro is @rank then 3
      when pro is @rank-1 then 1
      when pro < @rank-1 then 0
      when pro > @rank then 10*(pro-@rank)**2
    suma = Math.floor @progress/100
    if @rank < 0 and @rank + suma >= 0
      @rank += suma+1
    else
      @rank += suma
    @progress = unless @rank is 8 then @progress%100 else 0
_____________________________________
class User
  r=null
  constructor:->
    r=-8
    @rank=-8
    @progress=0
    return
  incProgress:(x)->
    if x<-8 or x>8 or x is 0 then throw new Exception()
    x-- if x>0
    if x is r then @progress+=3 else if x is r-1 then @progress++ else if x>r then @progress+=10*(x-r)**2
    if @progress>=100
      r+=@progress//100
      @progress-=100*(@progress//100)
    @rank=if r>=0 then r+1 else r
    @progress=0 if @rank is 8
    return
_____________________________________
class User 
  constructor: ->
    this.rank = -8;
    this.progress = 0;
  rank: ->
    return this.rank;
  progress: ->
    return this.progress;
  incProgress: (rank) ->
    # Make sure rank passed is valid
    if rank > 8 || rank < -8 || rank == 0
      throw "Outside range";
      return null;
    
    # Skip over 0 in difference calculations
    diff = Math.abs(this.rank - rank);
    if this.rank < 0 && rank > 0
      diff -= 1;
    
    if this.rank == 8
      # No progression once rank 8
      this.progress = 0;
    else
      if this.rank == rank + 1
        # Activity rank is one less than user
        this.progress += 1;
      else if this.rank == rank
        # Same rank
        this.progress += 3;
      else if rank > this.rank
        this.progress += 10 * diff * diff;
      else
        # Because kata description does not match tests
        this.progress += 1;
      
      this.incRank();
  incRank: ->
    if this.progress > 100 && this.rank != 8
      # Loop over progress and update rank for every 100 points
      while this.progress > 99
        this.rank += `(this.rank == -1) ? 2 : 1`;
        this.progress -= 100;
        
        # Reset progress if new rank is 8
        if this.rank == 8
          this.progress = 0;

