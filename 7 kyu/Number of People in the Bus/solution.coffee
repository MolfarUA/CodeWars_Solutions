number = (busStops) -> busStops.map( ([a,b]) -> a-b ).reduce( (t,s) -> t+s )
_____________________________________
number = (peopleListInOut) ->
  peopleListInOut.reduce ((a, [nIn, nOut]) -> a + nIn - nOut), 0
_____________________________________
number = (peopleListInOut) ->
  peopleListInOut.reduce ((acc, t) ->
    acc + t[0] - (t[1])
  ), 0
_____________________________________
number = (busStops) ->
  total = 0
  i = 0
  while i < busStops.length
    total += busStops[i][0]
    total -= busStops[i][1]
    i++
  total
_____________________________________
number = (busStops) -> busStops.reduce ((n, a) -> n + a[0] - (a[1])), 0
_____________________________________
number = (peopleListInOut) ->
  peopleListInOut.map((a)->a[0]-a[1]).reduce((a,b)->a+b)
