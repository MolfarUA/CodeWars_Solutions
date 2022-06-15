function isvalidwalk(walk)
  DIRECTIONS = Dict('n' => im, 'e' => 1, 's' => -im, 'w' => -1)
  return length(walk) == 10 && sum(DIRECTIONS[ch] for ch in walk) == 0
end
__________________________________________
dir = Dict('n' => [0,1], 's' => [0,-1], 'e' => [1,0], 'w' => [-1,0])

function isvalidwalk(walk)
  length(walk) == 10 && sum(map(d->dir[d], walk)) == [0,0]
end
__________________________________________
function isvalidwalk(walk)
  coords = [0, 0]
  d = Dict(
  'n' => () -> coords[2] += 1,
  's' => () -> coords[2] -= 1,
  'w' => () -> coords[1] -= 1,
  'e' => () -> coords[1] += 1
  )
  foreach(i -> d[i](), walk)
  length(walk) == 10 && coords == [0, 0]
end
__________________________________________
function isvalidwalk(walk)
  x, y = 0, 0
  if length(walk) != 10
    return false
  end
  for direction in walk
    if direction == 'n'
      y +=1
    elseif direction == 's'
      y -= 1
    elseif direction == 'e'
      x += 1
    elseif direction == 'w'
      x -= 1
    end
  end
  x == 0 && y == 0
end
__________________________________________
function isvalidwalk(walk)
  position = [0, 0]
  if length(walk) != 10
    return false
  else
    for step in walk
      if step == 'n'
        position[2] += 1
      elseif step == 's'
        position[2] -= 1
      elseif step == 'e'
        position[1] += 1
      else
        position[1] -= 1
      end
    end
    
    if position == [0, 0]
      return true
    else
      return false
    end
  end
end
