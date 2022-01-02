rules = [
  [1,3,1000]
  [6,3,600]
  [5,3,500]
  [4,3,400]
  [3,3,300]
  [2,3,200]
  [1,1,100]
  [5,1,50]
]

score = (dice) ->
  counts = {}
  for roll in dice
    counts[roll] = (counts[roll] or 0) + 1
  oldScore = newScore = 0
  loop
    oldScore = newScore
    for rule in rules when counts[rule[0]] >= rule[1]
      newScore += rule[2]
      counts[rule[0]] -= rule[1]
    return newScore if oldScore is newScore
_____________________________________________
score = (dice) ->
    factors = [0, 1000, 200, 300, 400, 500, 600]
    count = (dice.reduce(((a, b) -> a + (b == n)), 0) for n in [0..6])
    (count[1] % 3 * 100 + 
     count[5] % 3 * 50 +
     count.map((n, i) -> (n >= 3) * factors[i]).reduce (a, b) -> a + b)
_____________________________________________
# Three 1's => 1000 points
#  Three 6's =>  600 points
#  Three 5's =>  500 points
#  Three 4's =>  400 points
#  Three 3's =>  300 points
#  Three 2's =>  200 points
#  One   1   =>  100 points
#  One   5   =>   50 point

score = (dice) ->
  points = 0
  count = [0, 0, 0, 0, 0, 0]
  tripletPoints = [1000, 200, 300, 400, 500, 600]
  for num in dice when ++count[num - 1] is 3
    points += tripletPoints[num - 1]
    count[num - 1] = 0
  points += count[0] * 100 + count[4] * 50
_____________________________________________
score = (dice) ->
  thescore = 0
  counts = [0, 0, 0, 0, 0, 0, 0]
  dice.forEach (r) ->
    ++counts[r]
    if counts[r] is 3
      thescore += (if (r is 1) then 1000 else r * 100)
      counts[r] = 0

  thescore += counts[1] * 100 + counts[5] * 50
