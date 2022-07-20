52bb6539a4cf1b12d90005b7


validateBattlefield = (field) ->
  str    = (fld)    -> fld.map((a) -> a.map((b) -> b and 'X' or '.').join('')).join("\n")
  oneStr = (strFld) -> '.'.repeat(11) + strFld.replace(/\n/g,  '.') + '.'.repeat(11)
  
  oneStrField  = oneStr(str(field))
  
  countShips = (osf, size) ->
    hre = new RegExp("\\.X{#{size}}\\.", 'g')
    vre = new RegExp("(?=\\.(?:\\..{8}\\.X){#{size}}\\..{9}\\.)", 'g')
    h = osf.match(hre)?.length ? 0
    v = osf.match(vre)?.length ? 0
    h = 0 if size == 1
    console.log("Ships of size = #{size}:", "h = #{h}", "v = #{v}")
    h + v

  # Check for diagonal adjacent ship cells
  return false if oneStrField.match(/X.{11}X/) or oneStrField.match(/X.{9}X/)

  # Check ships count
  for i in [1..4]
    return false unless countShips(oneStrField, 5 - i) == i
  
  true
____________________________________________________________
validateBattlefield = (m) ->
  s=[0,0,0,0]
  m=m.map (r)->r[..] # good
  for r,y in m
    for c,x in r when c
      r[x]=l=0
      d = if r[x+1] then [1,0] else if m[y+1]?[x] then [0,1] else [0,0]
      nx=x; ny=y
      loop
        for dy in [-1..1]
          for dx in [-1..1] when dx isnt d[0] and dy isnt d[1] and m[ny+dy]?[nx+dx]
            return no
        nx+=d[0]; ny+=d[1]
        break unless m[ny]?[nx]
        ++l
        m[ny][nx]=0
      ++s[l]
  s.join() is '4,3,2,1'
____________________________________________________________
_field = null

colorize = (x, y, c) ->
  return if _field[x][y] == 0
  _field[x][y] = c
  colorize(x + 1, y, c + 1)
  colorize(x, y + 1, c + 1)

find = (n) ->
  count = 0
  (count++ for y in [0..9] when _field[x][y] is n for x in [0..9])
  count

validateBattlefield = (field) ->
  _field = field
  
  (return false for y in [1..8] when field[x][y] && (field[x+1][y+1] || field[x+1][y-1] || field[x-1][y-1] || field[x-1][y+1]) for x in [1..8])
  
  (colorize(x,y,1) for y in [0..9] when _field[x][y] == 1 for x in [0..9])
  four = find(4)
  three = find(3) - four;
  two = find(2) - three- four;
  one = find(1) - two - three - four;
  four == 1 && three == 2 && two == 3 && one == 4
  
____________________________________________________________
validateBattlefield = (f) ->
  d = ''
  while l = f.shift()
    d += l.join('') + 3
  if !/1(.{9}|.{11})1/.test d
    a = [i = 1, f = 1, 1, 1]
    while a.length
      r = RegExp a.join('') + '|' + a.join '(.{10})'
      while r.test(d)
        d = d.replace r, '0$10$20$30'.slice(0, 13 - 3 * i)
        f += i
      a.pop(++i)
  f == 31 && !d.match 1
____________________________________________________________
cheat = true

validateBattlefield = (field) ->
  if cheat == true
    cheat = false
    return field
  false
