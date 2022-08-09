568d0dd208ee69389d000016


rentalCarCost = (d) ->
  if d >= 7 then d * 40 - 50 else if d >= 3 then d * 40 - 20 else d * 40
__________________________
rentalCarCost = (d) ->
  m = d * 40
  if d > 2
    m -= 20
  if d > 6 
    m -= 30
  return m
__________________________
rentalCarCost = (d) ->
  x = 40
  d = switch 
    when d < 3 then d * x
    when d < 7 then (x * d) - 20
    else (x * d) - 50
__________________________
rentalCarCost = (n) -> if n<3 then n*40 else if n<7 then n*40-20 else n*40-50
