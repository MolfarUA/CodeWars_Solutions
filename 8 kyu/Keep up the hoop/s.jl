55cb632c1a5d7b3ad0000145


function hoopcount(n)
  n >= 10 ? "Great, now move on to tricks" : "Keep at it until you get it"
end
_____________________________
function hoopcount(n)
  n > 9 ? "Great, now move on to tricks" : "Keep at it until you get it"
end
_____________________________
function hoopcount(n)
  return n < 10 ? "Keep at it until you get it" : "Great, now move on to tricks"
end
_____________________________
function hoopcount(n)
  if n >= 10
    return "Great, now move on to tricks"
  end
  return "Keep at it until you get it"
end
