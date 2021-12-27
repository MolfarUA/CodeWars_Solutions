n = 7

range = (x) ->
  [0..(x - 1)]
  
div = (x, y) ->
  Math.floor x / y
  
neighbouringCells = range(n * n).map((id) ->
  range(n).map((i) ->
    i * n + id % n
  ).concat(range(n).map((i) ->
    div(id, n) * n + i
  )).filter (i) ->
    i != id
)

neighbouringUnits = range(2 * n * n).map((id) ->
  houseId = div(id, n) * n
  range(n).map((i) ->
    houseId + i
  ).filter (i) ->
    i != id
)

unitPairs = range(n * n).map((id) ->
  range(n).map (i) ->
    [
      div(id, n) * n + i
      (n + id % n) * n + i
    ]
)

generateBoard = ->
  range(n).map (i) ->
    range(n).fill 0

generateCellStates = ->
  range(n * n).map (_) ->
    range(n).fill(0).concat [
      n
      -1
    ]

generateUnitStates = ->
  range(2 * n * n).map (_) ->
    range(n).fill(0).concat [
      n
      -1
    ]

solvePuzzle = (clues) ->
  board = generateBoard()
  cells = generateCellStates()
  units = generateUnitStates()
  observers = clues.map((c, id) ->
    range(n).map((i) ->
      if id < n then id + i * n else if id < n * 2 then n - 1 - i + id % n * n else if id < n * 3 then n - 1 - (id % n) + (n - 1 - i) * n else i + (n - 1 - (id % n)) * n
    ).concat [ c ]
  )
  memento = [ [] ]

  pos = (c) ->
    board[~ ~(c / n)][c % n]

  look = (ts) ->
    m = -1
    ls = ts.map((e) ->
      m = Math.max(m, e)
      m
    )
    new Set(ls).size

  ccandidates = (c) ->
    cells[c].slice(0, n).map((v, i) ->
      [
        v
        i
      ]
    ).filter((t) ->
      t[0] == 0
    ).map (t) ->
      t[1]

  cisset = (c) ->
    cells[c][n + 1] != -1

  chas = (c, v) ->
    !cisset(c) and cells[c][v] == 0

  csize = (c) ->
    cells[c][n]

  cis = (c, v) ->
    cells[c][n + 1] == v

  cval = (c) ->
    cells[c][n + 1]

  ucell = (u, v) ->
    if u < n * n then div(u, n) * n + v else v * n + div(u - (n * n), n)

  ucandidates = (u) ->
    units[u].slice(0, n).map((v, i) ->
      [
        v
        i
      ]
    ).filter((t) ->
      t[0] == 0
    ).map (t) ->
      ucell u, t[1]

  uisset = (u) ->
    units[u][n + 1] != -1

  uhas = (u, v) ->
    !uisset(u) and units[u][if u < n * n then v % n else div(v, n)] == 0

  usize = (u) ->
    units[u][n]

  uis = (c, v) ->
    if units[c][n + 1] == u < n * n then v % n else div(v, n)

  uval = (u) ->
    units[u][n + 1]

  snapshot = ->
    memento.push []
    return

  restore = ->
    s = memento.pop()
    a = null
    while s.length > 0
      a = s.pop()
      a()
    return

  regundo = (a) ->
    memento[memento.length - 1].push a
    return

  uncloackCell = (cell, value) ->
    cells[cell][value]--
    if cells[cell][value] == 0
      cells[cell][n]++
    return

  uncloackUnit = (unit, value) ->
    units[unit][value]--
    if units[unit][value] == 0
      units[unit][n]++
    return

  cloackCell = (cell, value) ->
    cells[cell][value]++
    if cells[cell][value] == 1
      cells[cell][n]--
    return

  cloackUnit = (unit, value) ->
    units[unit][value]++
    if units[unit][value] == 1
      units[unit][n]--
    return

  unlockCell = (cell, value) ->
    cells[cell][n + 1] = -1
    return

  unlockUnit = (unit, value) ->
    units[unit][n + 1] = -1
    return

  lockCell = (cell, value) ->
    cells[cell][n + 1] = value
    return

  lockUnit = (unit, value) ->
    units[unit][n + 1] = value
    return

  uncloack = (cell, value) ->
    uncloackCell cell, value
    t = unitPairs[cell][value]
    rowUnit = t[0]
    colUnit = t[1]
    uncloackUnit rowUnit, cell % n
    uncloackUnit colUnit, div(cell, n)
    return

  cloack = (cell, value) ->
    regundo ->
      uncloack cell, value
      return
    cloackCell cell, value
    t = unitPairs[cell][value]
    rowUnit = t[0]
    colUnit = t[1]
    cloackUnit rowUnit, cell % n
    cloackUnit colUnit, div(cell, n)
    return

  unlock = (cell, value) ->
    board[div(cell, n)][cell % n] = 0
    unlockCell cell, value
    t = unitPairs[cell][value]
    rowUnit = t[0]
    colUnit = t[1]
    unlockUnit rowUnit, cell % n
    unlockUnit colUnit, div(cell, n)
    return

  lock = (cell, value) ->
    regundo ->
      unlock cell, value
      return
    board[div(cell, n)][cell % n] = value + 1
    lockCell cell, value
    t = unitPairs[cell][value]
    rowUnit = t[0]
    colUnit = t[1]
    lockUnit rowUnit, cell % n
    lockUnit colUnit, div(cell, n)
    i = 0
    while i < neighbouringCells[cell].length
      neighbouringCell = neighbouringCells[cell][i]
      cloack neighbouringCell, value
      i++
    j = 0
    while j < neighbouringUnits[rowUnit].length
      neighbouringRowUnit = neighbouringUnits[rowUnit][j]
      cloack cell, neighbouringRowUnit % n
      j++
    k = 0
    while k < neighbouringUnits[colUnit].length
      neighbouringColUnit = neighbouringUnits[colUnit][k]
      cloack cell, neighbouringColUnit % n
      k++
    return

  reduceEdgeClues = ->
    ii = 0
    while ii < observers.length
      o = observers[ii]
      switch o[o.length - 1]
        when 1
          if !cisset(o[0])
            lock o[0], n - 1
        when 2
          if chas(o[0], n - 1)
            cloack o[0], n - 1
          if chas(o[1], n - 2)
            cloack o[1], n - 2
        when n
          k = 0
          while k < n
            if !cisset(o[k])
              lock o[k], k
            k++
        else
          i = 0
          while i + 1 < o[o.length - 1]
            j = 0
            while j < o[o.length - 1] - 1 - i
              if chas(o[i], n - 1 - j)
                cloack o[i], n - 1 - j
              j++
            i++
          break
      ii++
    return

  reduceClues = ->
    ii = 0
    while ii < observers.length
      o = observers[ii]
      switch o[o.length - 1]
        when 2
          cnt = 0
          if cis(o[0], 0) and chas(o[1], n - 1)
            lock o[1], n - 1
            cnt++
          if cis(o[n - 1], n - 1) and chas(o[0], n - 2)
            lock o[0], n - 2
            cnt++
          if !chas(o[0], n - 2)
            b = -1
            i = 0
            while i < n
              if b == -1 and (chas(o[i], n - 1) or cis(o[i], n - 1))
                b = i
              i++
            l = 0
            while l < n
              if i <= b and chas(o[l], n - 2)
                cloack o[l], n - 2
                cnt++
              l++
            if chas(o[n - 1], n - 1)
              cloack o[n - 1], n - 1
              cnt++
          return cnt > 0
      ii++
    false

  reduceUniqueSingle = ->
    cell = 0
    while cell < cells.length
      if cisset(cell) or csize(cell) != 1
        cell++
        continue
      lock cell, ccandidates(cell)[0]
      return true
      cell++
    false

  reduceHiddenSingle = ->
    unit = 0
    while unit < units.length
      if uisset(unit) or usize(unit) != 1
        unit++
        continue
      lock ucandidates(unit)[0], unit % n
      return true
      unit++
    false

  reduceEdge = ->
    reduceEdgeClues()
    loop
      if reduceHiddenSingle()
        continue
      if reduceUniqueSingle()
        continue
      if reduceClues()
        continue
      break
    return

  reduce = ->
    loop
      if reduceClues()
        continue
      break
    return

  chooseNextConstraint = ->
    k = null
    m = n + 1
    i = 0
    while i < n * n
      if cisset(i)
        i++
        continue
      sz = csize(i)
      if sz < m
        xs = ccandidates(i)
        m = sz
        k = xs.map((v) ->
          [
            i
            v
          ]
        )
        if m < 2
          return k
      i++
    j = 0
    while j < 2 * n * n
      if uisset(j)
        j++
        continue
      zz = usize(j)
      if zz < m
        ys = ucandidates(j)
        m = zz
        k = ys.map((v) ->
          [
            v
            j % n
          ]
        )
        if m < 2
          return k
      j++
    k

  minMaxSeq = (o) ->
    seen = new Set
    seq = []
    i = 0
    res = []

    seek = ->
      if i == n
        res.push seq.map((_) ->
          _
        )
        return
      c = o[i]
      vs = []
      if cisset(c)
        vs.push cval(c)
      else
        ccandidates(c).forEach (v) ->
          vs.push v
          return
      vs = vs.filter((v) ->
        !seen.has(v)
      )
      if vs.size == 0
        return
      vi = 0
      while vi < vs.length
        v = vs[vi]
        seen.add v
        seq.push v
        i++
        seek()
        i--
        seq.pop()
        seen.delete v
        vi++
      return

    seek()
    ans = res.map((vi) ->
      [
        vi
        look(vi)
      ]
    )
    if !ans.length
      return [
        null
        null
      ]
    x = n + 1
    y = -1
    a = null
    b = null
    ii = 0
    while ii < ans.length
      t = ans[ii]
      vi = t[0]
      m = t[1]
      if m < x
        x = m
        a = vi
      if m > y
        y = m
        b = vi
      ii++
    [
      a
      b
    ]

  verify = (o) ->
    clue = o[n]
    if clue == 0
      return true
    t = minMaxSeq(o)
    a = t[0]
    b = t[1]
    if a == null or b == null
      return false
    if look(b) < clue or look(a) > clue
      return false
    true

  dfs = ->
    constraint = chooseNextConstraint()

    guard = ->
      observers.every verify

    if constraint == null
      return guard()
    i = 0
    while i < constraint.length
      t = constraint[i]
      cell = t[0]
      value = t[1]
      snapshot()
      lock cell, value
      reduce()
      if guard() and dfs()
        return true
      restore()
      i++
    false

  reduceEdge()
  dfs()
  board
______________________________________________________
merge = (a, b) -> b.map((x) -> [].concat(a, x))
perms = (arr) ->
  return [arr] if arr.length == 1
  [0...arr.length].reduce ((p, i) -> p.concat merge arr[i], perms arr[0...i].concat arr[(i + 1)...]), []

lclueFor = (vector) ->
  [clue, max] = [0, 0]
  for a in vector
    if a > max
      clue += 1
      max = a
  clue

rclueFor = (vector) -> lclueFor ([vector...]).reverse()

vectorsByClues = (vectors) ->
  vectors.reduce(((acc, vector) ->
    [l, r] = [lclueFor(vector), rclueFor(vector)]
    for k in ["#{l}_#{r}", "0_#{r}", "#{l}_0"]
      acc[k] ?= []
      acc[k].push vector
    acc
  ), {})

vectorsFilterCross  = (vectors, i, v) -> vectors.filter (a) -> a[i] == v
vectorsFilterSide   = (vectors, i, v) -> vectors.filter (a) -> a[i] != v

isComplete      = (matrix) -> 0 not in [].concat(matrix...)
matrixCopy      = (matrix) -> matrix.map (row) -> [row...]
matrixToString  = (matrix) -> matrix.map((row) -> row.join(' ')).join('\n')
matrixCreate    = (size)   -> [0...size].map(-> Array(size).fill(0))
matrixGetRow    = (matrix, i) -> matrix[i]
matrixGetCol    = (matrix, j) -> matrix.map (row) -> row[j]
matrixPutRow    = (matrix, i, row) ->
  res = matrixCopy matrix
  res[i] = [row...]
  res
matrixPutCol    = (matrix, j, col) ->
  res = matrixCopy matrix
  (row[j] = col[i]) for i, row of res
  res
matrixPutVector = (matrix, [cr, index], vector) -> ({col: matrixPutCol, row: matrixPutRow})[cr](matrix, index, vector)

statePush           = (stack, state) -> stack.push state
statePop            = (stack)        -> stack.pop()
statePopVariant     = (state, [cr, index]) -> state["#{cr}Variants"]?[index]?.pop()
stateDeleteVariants = (state, [cr, index]) -> delete state["#{cr}Variants"][index]
stateNextPosition   = (state) ->
  [minSize, minKind, minIndex] = [Infinity, null, -1]
  for cr in ['row', 'col']
    for k, v of state["#{cr}Variants"]
      [minSize, minKind, minIndex] = [v.length, cr, k] if v.length and minSize > v.length
  [minKind, +minIndex]

stateFilterVariants = (state, [cr, index], vector) ->
  res = {colVariants: {}, rowVariants: {}}
  crossVariants = "#{({row: 'col', col: 'row'})[cr]}Variants"
  variants      = "#{cr}Variants"
  for k, rv of state[crossVariants]
    res[crossVariants][k] = vectorsFilterCross rv, index, vector[+k]
  for k, rv of state[variants]
    continue if index == +k
    res[variants][k] = vectorsFilterSide rv, +k, vector[+k]
  res

stateHasVariants = (state) ->
  for variants in ['rowVariants', 'colVariants']
    for k, rv of state[variants]
      return false unless rv.length
  true

stateCrossVariants = ({colVariants, rowVariants}, size = 7) ->
  res = {colVariants: {}, rowVariants: {}}
  filter = (colVariants, rowVariants) ->
    filtered = {}
    possibleCells = matrixCreate(size).map((row) -> row.map(-> new Set()))
    possibleCells[+i][j].add(cell) for j, cell of row for row in rows for i, rows of rowVariants
    filtered[j] = cols.filter((col) -> col.reduce(
      ((acc, cell, i) -> acc and possibleCells[i][+j].has(cell)),
      true
    )) for j, cols of colVariants
    filtered
  res.colVariants = filter(colVariants, rowVariants)
  res.rowVariants = filter(rowVariants, res.colVariants)
  res

initialState = (clues) ->
  size = clues.length / 4
  state = {matrix: matrixCreate(size), colVariants: {}, rowVariants: {}}
  $perms = perms([1..size])
  $vectorsByClues = vectorsByClues($perms)
  for i in [0...size] # cols
    [cl, cr] = [clues[i], clues[size * 3 - 1 - i]]
    [rl, rr] = [clues[size * 4 - 1 - i], clues[size + i]]
    state.colVariants["#{i}"] = $vectorsByClues["#{cl}_#{cr}"] ? $perms
    state.rowVariants["#{i}"] = $vectorsByClues["#{rl}_#{rr}"] ? $perms
  state.current = stateNextPosition(state)
  state = Object.assign(state, stateCrossVariants(state))
  state

solvePuzzle = (clues) ->
  stack = []
  state = initialState(clues)
  loop
    vector = statePopVariant(state, state.current)
    unless vector
      state = statePop(stack)
      return false unless state
      continue
    statePush(stack, state)
    state = Object.assign {
      matrix: matrixPutVector(state.matrix, state.current, vector)
      current: state.current
    }, stateFilterVariants(state, state.current, vector)
    unless stateHasVariants(state)
      state = statePop(stack)
      continue
    return state.matrix if isComplete(state.matrix)
    state.current = stateNextPosition(state)

  state.matrix
____________________________________________
permutes = ( arr )->
  p = arr[..]
  [i,l,o]=[1,p.length,[p[..]]]
  c = Array(l).fill 0

  while i < l
    if c[i] < i
      k = i%2 and c[i]
      [p[i],p[k]] = [p[k],p[i]]
      ++c[i]
      i = 1
      o.push p[..]
    else
      c[i] = 0
      ++i
  o

[qps,keys,W] = [{},[]]

calc = (w)->
  l=r=1
  w.reduce (a,b)-> if a<b then (++l; b) else a
  w.reduceRight (a,b)-> if a<b then (++r; b) else a
  [l,r]


precalc = (w)->
  return if w is W and keys.length
  W=w
  keys=for y in [0..w]
    for x in [0..w]
      x+','+y

  qps['0,0']=permutes [1..w]
  for v in qps['0,0']
    [l,r]=k=calc v
    qps[keys[l][r]]?=[]
    qps[keys[l][r]].push v
    qps[keys[l][0]]?=[]
    qps[keys[l][0]].push v
    qps[keys[0][r]]?=[]
    qps[keys[0][r]].push v
  return


len = (v)-> v.length
nb = (n)-> 1<<(n-1)
bn = (b)->
  o=1
  ++o while b>>=1
  o


class Grid
  constructor: (@rps,@cps)->
    @w=@rps.length
    @o=([] for [0...@w])
    @s=(0 for [0...@w] for [0...@w])
    @build()

  build: (re)->
    @g = for r,y in @rps
      for c,x in @cps
        if @o[y][x]? then 0
        else
          r.reduce(((a,v)->a|nb(v[x])),0) & c.reduce ((a,v)->a|nb(v[y])),0
    return

  sieve: ->
    loop
      o=ch
      ch=0
      for r,y in @g
        for c,x in r when c
          if 0 is (c&(c-1)) # single bit
            for i in [0...@w]
              @g[y][i]&=~ch=c if i isnt x and (c&@g[y][i])
              @g[i][x]&=~ch=c if i isnt y and (c&@g[i][x])
          else
            br=bc=c
            for i in [0...@w]
              br&=~@g[y][i] if i isnt x
              bc&=~@g[i][x] if i isnt y
            if br or bc
              c&=br if br
              c&=bc if bc
              @g[y][x]=c
              for i in [0...@w]
                @g[y][i]&=~ch=c if i isnt x and (c&@g[y][i])
                @g[i][x]&=~ch=c if i isnt y and (c&@g[i][x])
      break unless ch
    o

  reduce: ->
    for r,y in @g
      for c,x in r when c
        @rps[y] = (rp for rp in @rps[y] when c&nb(rp[x]) or rp[x] is @o[y][x])
        @cps[x] = (cp for cp in @cps[x] when c&nb(cp[y]) or cp[y] is @o[y][x])
        if c and (c&(c-1)) is 0
          @o[y][x]=bn c
          @g[y][x]=0
    @build 1
    return

solvePuzzle = (qs)->
  w = qs.length/4
  precalc w
  rps=[];cps=[]
  for i in [0...w]
    rps[i]=qps[ keys[ qs[4*w-i-1] ][ qs[w+i] ] ]
    cps[i]=qps[ keys[ qs[i] ][ qs[3*w-i-1] ] ]
  grid = new Grid rps,cps
  while grid.sieve()
    grid.reduce()
  grid.o
