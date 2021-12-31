class Elevator
  constructor: (@capacity) ->
    @destinations = []
    @stops = []

  handle: (@queues) ->
    @stopAt(0)
    @operate()
    @stopAt(0)
    @stops

  stopAt: (floor) ->
    return if floor == @current_floor
    @current_floor = floor
    @stops.push(floor)

  operate: ->
    for floor from @nextFloor()
      break if @allPassengersServed()
      continue unless @shouldStopAt(floor)
      @stopAt(floor)
      @letPassengersExit()
      @letPassengersEnter()

  nextFloor: ->
    floor = @current_floor - 1
    @direction = 'up'

    loop
      if @direction == 'up'
        floor += 1
        @direction = 'down' if floor == @queues.length - 1
      else
        floor -= 1
        @direction = 'up' if floor == 0

      yield floor

  allPassengersServed: ->
    @destinations.length == 0 && @floorsWithQueues().length == 0

  floorsWithQueues: ->
    index for queue, index in @queues when queue.length > 0

  shouldStopAt: (floor) ->
    return true if floor in @destinations

    isTravellingInCurrentDirection = (destination) => if @direction == 'up' then destination > floor else destination < floor
    @queues[floor].filter(isTravellingInCurrentDirection).length > 0

  letPassengersExit: ->
    @destinations = @destinations.filter (floor) => floor != @current_floor

  letPassengersEnter: ->
    queue = @queues[@current_floor]
    destinations = -> queue.filter(isTravellingInCurrentDirection)
    isTravellingInCurrentDirection = (destination) => if @direction == 'up' then destination > @current_floor else destination < @current_floor

    while destinations().length > 0 && @destinations.length < @capacity
      floor = destinations()[0]
      queue.splice(queue.indexOf(floor), 1)
      @destinations.push(floor)

theLift = (queues, capacity) ->
  new Elevator(capacity).handle(queues)

___________________________________________________
theLift = (qs, cap)->
  [o,r,ol]=[[0],[],-1]
  T=qs.length-1
  push=(y)->if o[o.length-1]!=y then o.push y
  while ol!=o.length
    ol=o.length
    for [a,b,d] in [[0,T,1],[T,0,-1]]
      for y in [a..b] by d
        q=[]
        rl=r.length
        r=r.filter (v)->v!=y
        if rl!=r.length then push y
        for c in qs[y]
          if d==Math.sign c-y
            push y
            if cap>r.length then r.push c else q.push c
          else
            q.push c
        qs[y]=q
  push 0
  return o
