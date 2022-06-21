5870fa11aa0428da750000da


execute = (code, d = 0, res = [[0,0]]) =>
  dir = [
    ([x, y]) => [x+1, y]
    ([x, y]) => [x, y+1]
    ([x, y]) => [x-1, y]
    ([x, y]) => [x, y-1]
  ]
  ops =
    L: () => d = (d+1)%4
    R: () => d = (d+4-1)%4
    F: ()=> res[i=res.length] = dir[d] res[i-1]
  code
    .replace /\d+/g, (el, i, w) => w[i-1].repeat el-1
    .replace /./g,   (el, i)    => do ops[el]
  [xi, yi, xa, ya] = res
    .reduce (([xi, yi, xa, ya], [x, y]) => [Math.min(xi, x), Math.min(yi, y), Math.max(xa, x), Math.max(ya, y)])
      , [0, 0, 0, 0]
  [ya..yi].map (y) =>
    [xi..xa].map (x) => ' *'[+!!res.find (xy) => xy[0] == x && xy[1] == y]
    .join('')
  .join('\r\n')
__________________________
execute=(s)->
  map=[['*']]; x=y=d=t=l=r=0
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
execute = (code) ->
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

  for letter in code.replace(/([FLR])(\d+)/g, (all, letter, count) => letter.repeat count * 1)
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
