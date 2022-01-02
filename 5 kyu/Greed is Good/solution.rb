SCORE_MAP = {
  1 => [0, 100, 200, 1000, 1100, 1200, 2000],
  2 => [0, 0, 0, 200, 200, 200, 400],
  3 => [0, 0, 0, 300, 300, 300, 600],
  4 => [0, 0, 0, 400, 400, 400, 800],
  5 => [0, 50, 100, 500, 550, 600, 1000],
  6 => [0, 0, 0, 600, 600, 600, 1200]
}

def score( dice )
  (1..6).inject(0) do |score, die|
    score += SCORE_MAP[die][dice.count(die)]
  end
end
_____________________________________________
def score( dice )
  [ dice.count(1) / 3 * 1000,
    dice.count(6) / 3 * 600,
    dice.count(5) / 3 * 500,
    dice.count(4) / 3 * 400,
    dice.count(3) / 3 * 300,
    dice.count(2) / 3 * 200,
    dice.count(1) % 3 * 100,
    dice.count(5) % 3 * 50 ].reduce(:+)
end
_____________________________________________
def score( dice )
  m = {1 => 100, 5 => 50}
  (1..6).reduce(0) do|res, i|
    count = dice.count(i)    
    res + count/3 * i * (i==1 ? 1000 : 100) + count%3*(m[i].to_i)
  end
end
_____________________________________________
def score(dice)
  dice.sort.join.gsub(/(\d)\1\1|(1|5)/).inject(0) do |sum, num|
    sum + ($1.to_i * 100 + $2.to_i * 10 ) * (num[0] == '1' ? 10 : 1)
  end
end
_____________________________________________
GREED_SCORES = {
  1 => [0, 100, 200, 1000, 1100, 1200],
  2 => [0, 0, 0, 200, 200, 200],
  3 => [0, 0, 0, 300, 300, 300],
  4 => [0, 0, 0, 400, 400, 400],
  5 => [0, 50, 100, 500, 550, 600],
  6 => [0, 0, 0, 600, 600, 600]
}

def score(dice)
  GREED_SCORES.keys.inject(0) do |score, key|
    score + GREED_SCORES[key][dice.count(key)]
  end
end
