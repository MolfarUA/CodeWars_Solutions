58738d518ec3b4bf95000192


execute=(s)->
  map=[['*']]; x=y=d=t=l=r=0
  while '(' in s
    s=s.replace /\(([^()]*)\)(\d*)/g, (_,p1,p2)->if p2.length then Array(+p2+1).join p1 else p1
  for m in s.match(/[LRF]\d*/g) ?[]
    c=m[0]; n=+(m[1..] or 1)
    {
      L: -> d=(d-n)%%4; return
      R: -> d=(d+n)%%4; return
      F: ->
        while n--
          map[y+=(2-d)%2]?=[]
          map[y][x+=(1-d)%2]='*'
          t=y if t>y; l=x if l>x; r=x if x>r
        return
    }[c]()
  ((map[y][x] ?' ' for x in [l..r]).join '' for y in [t...map.length]).join '\r\n'
__________________________
executeRS1 = (code) ->
  marks = [[0, 0]]
  grid =
    '0;0': true
  direction = 0
  directions = [
    [1, 0]
    [0, 1]
    [-1, 0]
    [0, -1]
  ]

  for letter in code.replace(/([FLR])(\d+)/g, (all, letter, repeater) => letter.repeat repeater * 1)
    switch letter
      when 'F'
        mark = marks[marks.length - 1].slice()
        mark[0] += directions[direction][0]
        mark[1] += directions[direction][1]
        grid[mark[0] + ';' + mark[1]] = true
        marks.push mark
      when 'L'
        direction = (direction + 3) % 4
      when 'R'
        direction = (direction + 1) % 4

  minX = marks.reduce ((base, mark) -> Math.min(base, mark[0])), 0
  maxX = marks.reduce ((base, mark) -> Math.max(base, mark[0])), 0
  minY = marks.reduce ((base, mark) -> Math.min(base, mark[1])), 0
  maxY = marks.reduce ((base, mark) -> Math.max(base, mark[1])), 0

  [minY..maxY].map((y) ->
    [minX..maxX].map((x) -> if grid[x + ';' + y]
      '*'
    else
      ' '
    ).join ''
  ).join '\r\n'

execute = (code)->
  rs1Code = null

  while rs1Code isnt code
    rs1Code = code
    code = code.replace /\(([^()]*)\)(\d+)?/, (all, pattern, repeater) ->
      pattern.repeat if repeater then repeater | 0 else 1

  executeRS1 code
