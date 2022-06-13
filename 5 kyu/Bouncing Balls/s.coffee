bouncingBall = (h, bounce, window) ->
  if h <= 0 || bounce <= 0 || bounce >= 1 || window >= h
    return -1
  count = 1
  while h > window
    h *= bounce
    count += 2
  count - 2
_______________________________________________
bouncingBall = (h, bounce, window) ->
    if h <= 0 or window >= h or bounce <= 0 or bounce >= 1
      return -1
    seen = -1
    while h > window
      seen += 2
      h = h * bounce
    seen
_______________________________________________
bouncingBall = (h, bounce, window) ->
  if h < 0 or bounce <= 0 or bounce >= 1 or window >= h
    -1
  else
    2 + bouncingBall(h * bounce, bounce, window)
_______________________________________________
bouncingBall = (h, bounce, window) ->
  if h <= 0 || bounce <= 0 || bounce >= 1 || window >= h
    return -1
  return 2 + bouncingBall(h*bounce, bounce, window)
