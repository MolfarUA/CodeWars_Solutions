576757b1df89ecf5bd00073b


towerBuilder = (floors) ->
  (padding = " ".repeat floors - i - 1) + "*".repeat(2 * i + 1) + padding for i in [0...floors]
_____________________________
towerBuilder = (n) -> Array.from(Array(n),(_,i)->
  a=--n
  b=1+i*2
  ' '.repeat(a)+'*'.repeat(b)+' '.repeat(a))
_____________________________
towerBuilder = (nFloors) ->
  result = []
  floor = 0
  while floor < nFloors
    beginOrEnd = Array(nFloors - floor).join(' ')
    center = Array(floor * 2 + 2).join('*')
    result.push beginOrEnd + center + beginOrEnd
    floor += 1
  result
_____________________________
towerBuilder = (nFloors) ->
  a = []
  
  width = nFloors * 2 - 1  
  for floor in [1..nFloors]
    starsCount = floor * 2 - 1
    sideSpacesCount = Math.floor((width - starsCount) / 2)
    a.push(" ".repeat(sideSpacesCount) + "*".repeat(starsCount) + " ".repeat(sideSpacesCount))
    
  a
_____________________________
towerBuilder = (nFloors) ->
  tower = []
  i = 1
  while i <= nFloors
    s = ' '.repeat(nFloors - i)
    t = '*'.repeat(2 * i - 1)
    tower.push s + t + s
    i++
  tower
_____________________________
towerBuilder = (n) ->
  [n..1].map (index)->
    prefix  = '*'.repeat n - index
    spacing = ' '.repeat index - 1
    return  spacing + prefix + '*' + prefix + spacing
