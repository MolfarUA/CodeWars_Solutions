56f173a35b91399a05000cb7


function findlongest(str)
  maximum(length, split(str))
end
__________________________
findlongest(s) = maximum(length, split(s))
__________________________
function findlongest(s)
  maximum(length(w) for w in split(s))
end
__________________________
function findlongest(str)
  return maximum(length(s) for s in split(str," "))
end
