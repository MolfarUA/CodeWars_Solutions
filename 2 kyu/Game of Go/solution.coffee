NS=[[1,0],[0,1],[-1,0],[0,-1]]
class Go
  constructor: (@h,@w)->
    @w?=@h
    @size=height:@h,width:@w
    throw new Error 'board too large (>25)' if @h>25 or @w>25
    @reset()

  reset: ->
    @board=('.' for [0...@w] for [0...@h])
    @hist=[]
    @_next 0
    @hasHandi=false
    return

  _p:(m)->
    {y:@h-m[...-1], x:'ABCDEFGHJKLMNOPQRSTUVWXYZ'.indexOf m[-1..]}

  _next:(@t=1-@t)->
    @turn=['black','white'][@t]
    @hist.push JSON.stringify @board
    return

  _find:(x,y,f)->
    p=@board[y][x]
    next=[[x,y]]
    walk=(r[..] for r in @board)
    while next.length
      cur=next
      next=[]
      for [x,y] in cur
        [c,walk[y][x]]=[walk[y][x],null]
        return {x,y} if typeof f is 'string' and c is f
        if c is p
          f x,y if typeof f is 'function'
          for [dx,dy] in NS when (c=walk[ny=y+dy]?[nx=x+dx])?
            next.push [nx,ny]
    return

  getPosition: (a)->
    {x,y}=@_p a
    @board[y][x]

  move: (args...)->
    for m in args
      {x,y}=@_p m
      throw new Error 'invalid move' if '.' isnt @board[y]?[x]
      @board[y][x]='xo'[@t]
      for [dx,dy] in NS when 'ox'[@t] is @board[ny=y+dy]?[nx=x+dx]
        # check capture
        unless @_find nx,ny, '.'
          @_find nx,ny, (x,y)=>
            @board[y][x]='.'
            return

      # check self-capture
      unless @_find x,y,'.'
        @board[y][x]='.'
        throw new Error 'self-capture is not allowed'

      @_next()

      # check Ko cycle
      if @hist[@hist.length-1] is @hist[@hist.length-3]
        @rollback 1
        throw new Error 'Ko cycle is not allowed'
    return

  pass: ->
    @_next()
    return

  rollback: (n)->
    throw new Error 'rollback to before the game started?' if n >= @hist.length
    @hist=@hist[...-n]
    @t=@hist.length%2
    @board=JSON.parse @hist.pop()
    @_next()
    return

  handicapStones: (n)->
    c=(@w-1)/2; l=[2,3][+(@w>9)]; r=c+c-l
    hs=[[r,l],[l,r],[r,r],[l,l],[c,c],[l,c],[r,c],[c,l],[c,r]]
    hs = switch "#{@w}x#{@h}"
        when '9x9' then hs[...5]
        when '13x13','19x19' then hs
    throw new Error 'no handicaps for you' unless @hist.length is 1 and n <= hs?.length and @hasHandi==false
    @hasHandi=true
    for [x,y] in hs[...n]
      @board[y][x]='x'
    return
