55cb632c1a5d7b3ad0000145


def hoop_count(n)
  n < 10 ? "Keep at it until you get it" :  "Great, now move on to tricks"
end
_____________________________
def hoop_count n
  n <= 9 ? "Keep at it until you get it" : "Great, now move on to tricks"
end
_____________________________
def hoop_count n
  return 'Keep at it until you get it' if n < 10
  'Great, now move on to tricks'
end
hoop_count(3)
hoop_count(11)
_____________________________
def hoop_count n
  n >= 10 ? "Great, now move on to tricks" : "Keep at it until you get it"
end
