def score(dice): 
  sum = 0
  counter = [0,0,0,0,0,0]
  points = [1000, 200, 300, 400, 500, 600]
  extra = [100,0,0,0,50,0]
  for die in dice: 
    counter[die-1] += 1
  
  for (i, count) in enumerate(counter):
    sum += (points[i] if count >= 3 else 0) + extra[i] * (count%3)

  return sum 
_____________________________________________
def score(dice):
    return dice.count(1)//3 * 1000 + dice.count(1)%3 * 100 \
           + dice.count(2)//3 * 200 \
           + dice.count(3)//3 * 300 \
           + dice.count(4)//3 * 400 \
           + dice.count(5)//3 * 500 + dice.count(5)%3 * 50 \
           + dice.count(6)//3 * 600 \
_____________________________________________
def score(dice):
    # dice scores  [1   ,   2,   3,   4, 5,   6]
    scores_3same = [1000, 200, 300, 400, 500, 600]
    scores_single = [100 ,   0,   0,   0,  50,   0]
    
    sum = 0
    for i in range(1,7):
        count_i = dice.count(i)
        sum += (count_i // 3) * scores_3same[i-1] + (count_i % 3) * scores_single[i-1]
            
    return sum
_____________________________________________
from collections import Counter as count

def score(dice):
    threes, ones, c = {1: 1000, 6: 600, 5: 500, 4: 400, 3: 300, 2: 200}, {1: 100, 5: 50}, count(dice)
    return sum((c[v]//3)*threes[v] + (c[v]%3)*ones.get(v, 0) for v in c)
_____________________________________________
SCORES = [
  # triples
  ["111", 1000],
  ["666", 600],
  ["555", 500],
  ["444", 400],
  ["333", 300],
  ["222", 200],
  # singles
  ["1", 100],
  ["1", 100],
  ["5", 50],
  ["5", 50] ]


def score(dice):
    dice = "".join(str(d) for d in sorted(dice))
    total = 0
    
    for key, val in SCORES:
        if key in dice:
            total += val
            dice = dice.replace(key, "", 1)
    
    return total
_____________________________________________
def score(dice):
    sum, c1, c5 = 0, dice.count(1), dice.count(5)
    if c1 >= 3:
        c1 -= 3
        sum += 1000
    sum += 100 * c1
    
    if c5 >= 3:
        c5 -= 3
        sum += 500
    sum += 50 * c5
    
    if dice.count(6) >= 3: sum += 600
    if dice.count(4) >= 3: sum += 400
    if dice.count(3) >= 3: sum += 300
    if dice.count(2) >= 3: sum += 200
    return sum
_____________________________________________
score=lambda d:100*(sum(i+9*(i==1)for i in range(7)if d.count(i)>2)+d.count(1)%3+d.count(5)%3/2)
_____________________________________________
from collections import Counter
from itertools import starmap

def getPoints(side,n):
    (some3,r), ratio = divmod(n,3), 100*10**(side==1) * side
    return some3 * ratio + r * (side in (1,5)) * ratio//10

def score(dice):
    return sum(starmap(getPoints, Counter(dice).items()))
_____________________________________________
def score(dice):
    diceList = [d for d in dice]
    rules = [(3,1,1000),(3,6,600),(3,5,500),(3,4,400),(3,3,300),(3,2,200),(1,1,100),(1,5,50)]
    score = 0
    continueIterations = 1
    while continueIterations:
        for times, value, points in rules:
            if (diceList.count(value) >= times):
                score += points
                for t in range(0,times): diceList.remove(value)
                continueIterations = 1
                break
            else:
                continueIterations = 0
    return score
_____________________________________________
def score(dice):
    total = 0
    for d in range(1, 7):
        count = dice.count(d)
        if count >= 3:
            total += 1000 if d == 1 else d * 100
            count -= 3
        total += 100 * count if d == 1 else 50 * count if d == 5 else 0
    return total
_____________________________________________
def score(dice):
    score, data = 0, {1:(0,100,200,1000,1100,1200),
                      2:(0,0,0,200,200,200),
                      3:(0,0,0,300,300,300),
                      4:(0,0,0,400,400,400),
                      5:(0,50,100,500,550,600),
                      6:(0,0,0,600,600,600)}
    for i in data:
        score += (data[i][dice.count(i)])
    return score
