55cb632c1a5d7b3ad0000145


hoopCount = (n) ->
  if n >= 10 then "Great, now move on to tricks" else "Keep at it until you get it"
_____________________________
hoopCount = (n) ->
  if n < 10 then 'Keep at it until you get it' else 'Great, now move on to tricks' 
_____________________________
hoopCount = (n) ->
  if n < 10
      "Keep at it until you get it"
  else
      "Great, now move on to tricks"
_____________________________
hoopCount = (n) -> if n <= 9 then "Keep at it until you get it" else "Great, now move on to tricks"
