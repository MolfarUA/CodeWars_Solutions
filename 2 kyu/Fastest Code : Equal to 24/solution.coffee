forms = 
  '((x1y)2z)3w': (x, y, z, w, o1, o2, o3) ->
    o3 o2(o1(x, y), z), w
  '(x1y)2(z3w)': (x, y, z, w, o1, o2, o3) ->
    o2 o1(x, y), o3(z, w)
  '(x1(y2z))3w': (x, y, z, w, o1, o2, o3) ->
    o3 o1(x, o2(y, z)), w
  'x1(y2(z3w))': (x, y, z, w, o1, o2, o3) ->
    o1 x, o2(y, o3(z, w))
  'x1((y2z)3w)': (x, y, z, w, o1, o2, o3) ->
    o1 x, o3(o2(y, z), w)
op = 
  '+': (a, b) ->
    a + b
  '-': (a, b) ->
    a - b
  '*': (a, b) ->
    a * b
  '/': (a, b) ->
    a / b
ts = [ '+', '-', '*', '/' ]

equalTo24 = (a, b, c, d) ->
  numbers = [
    [a,b,c,d],[a,b,d,c],[a,c,b,d],[a,c,d,b],[a,d,b,c],[a,d,c,b],
    [b,a,c,d],[b,a,d,c],[b,c,a,d],[b,c,d,a],[b,d,a,c],[b,d,c,a],
    [c,b,a,d],[c,b,d,a],[c,a,b,d],[c,a,d,b],[c,d,b,a],[c,d,a,b],
    [d,b,c,a],[d,b,a,c],[d,c,b,a],[d,c,a,b],[d,a,b,c],[d,a,c,b]
  ]
  i = 0
  while i < numbers.length
    x = numbers[i][0]
    y = numbers[i][1]
    z = numbers[i][2]
    w = numbers[i][3]
    o1 = 0
    while o1 < ts.length
      o2 = 0
      while o2 < ts.length
        o3 = 0
        while o3 < ts.length
          form = 0
          while form < Object.keys(forms).length
            r = Object.keys(forms)[form]
            if Math.abs(forms[r](x, y, z, w, op[ts[o1]], op[ts[o2]], op[ts[o3]]) - 24) < 1e-6
              return r.replace('1', ts[o1]).replace('2', ts[o2]).replace('3', ts[o3]).replace('x', x).replace('y', y).replace('z', z).replace('w', w)
            form++
          o3++
        o2++
      o1++
    i++
  'It\'s not possible!'
_____________________________________________
np = "It's not possible!"

para = (s) => 
  if (/[-+\*\/]/.test(s)) &&!/^\(.*\)$/.test(s)
    return "("+s+")"
  return s

abs=Math.abs

eq = (r) => (x) => abs(x-r)<1e-8

solve2 = (sx,x,sy,y,r) =>
  sub=np
  sub=sx+"+"+sy if sub==np && eq(r)(x+y)
  sub=sx+"-"+para(sy) if sub==np && eq(r)(x-y)
  sub=sy+"-"+para(sx) if sub==np && eq(r)(y-x)
  sub=para(sx)+"*"+para(sy) if sub==np && eq(r)(x*y)
  sub=para(sx)+"/"+para(sy) if sub==np && y!=0 && abs(y)<=abs(x) && eq(r)(x/y)
  sub=para(sy)+"/"+para(sx) if sub==np && x!=0 && abs(x)<=abs(y) && eq(r)(y/x)
  return sub

solve1_ = (sx,x,a,r) =>
  if a.length==0
    return eq(r)(x) ? sx : np 
  if a.length==1
    return sx+"+"+a[0] if eq(r)(x+a[0])
    return sx+"-"+a[0] if eq(r)(x-a[0])
    return a[0]+"-"+para(sx) if eq(r)(a[0]-x)
    return para(sx)+"*"+a[0] if eq(r)(x*a[0])
    return para(sx)+"/"+a[0] if a[0]!=0 && eq(r)(x/a[0])
    return a[0]+"/"+para(sx) if x!=0 && eq(r)(a[0]/x)
    return np
  if a.length==2
    [y,z]=a
    sub=np
    sub=solve2 sx,x,""+y+"+"+z,y+z,r if sub==np
    sub=solve2 sx,x,""+y+"-"+z,y-z,r if sub==np
    sub=solve2 sx,x,""+z+"-"+y,z-y,r if sub==np
    sub=solve2 sx,x,""+y+"*"+z,y*z,r if sub==np
    sub=solve2 sx,x,""+y+"/"+z,y/z,r if sub==np && z!=0
    sub=solve2 sx,x,""+z+"/"+y,z/y,r if sub==np && y!=0 
    return sub if sub!=np
  for y, i in a
    a1=a.filter((_,j)=>j!=i)
    sub=solve1 "("+sx+"+"+y+")",x+y,a1,r
    if sub!=np
      return sub
    sub=solve1 ""+sx+"*"+y,x*y,a1,r
    if sub!=np
      return sub
    sub=solve1 "("+sx+"-"+y+")",x-y,a1,r
    if sub!=np
      return sub
    sub=solve1 "("+y+"-"+para(sx)+")",y-x,a1,r
    if sub!=np
      return sub
    if y!=0 
      sub=solve1 ""+sx+"/"+y,x/y,a1,r
      if sub!=np
        return sub
    if x!=0
      sub=solve1 ""+y+"/"+para(sx),y/x,a1,r
      if sub!=np
        return sub
    sub=solve1 sx,x,a1,r-y
    return ""+y+"+"+sub if sub!=np
    sub=solve1 sx,x,a1,r+y
    return ""+sub+"-"+y if sub!=np
    sub=solve1 sx,x,a1,y-r
    return ""+y+"-"+"("+sub+")" if sub!=np
    if y!=0
      sub=solve1 sx,x,a1,r/y
      return y+"*"+para(sub) if sub!=np
    sub=solve1 sx,x,a1,r*y
    return para(sub)+"/"+y if sub!=np
  return np

solve1 = (sx,x,a1,r) =>
  sub=solve1_ sx,x,a1,r
  console.log(sx,x,a1,r,sub) if sub!=np
  return sub

equalTo24 = (a,b,c,d) -> 
  e=[a,b,c,d]
  for x,i in e
    a1=e.filter((_,j)=>j!=i)
    sub=solve1 ""+x,x,a1,24
    return sub if sub!=np
  return np

_____________________________________________
to_n = (x) -> if 'number' == typeof x then x else to_n x[0]

rpn2infix = (rpn) ->
  st = []
  for t in rpn
    if t in '+-*/'
      [b, a] = [st.pop(), st.pop()]
      st.push([a, t, b])
      continue
    st.push(t)
  st[0]

evalRpn = (rpn) ->
  st = []
  for t in rpn
    if t in '+-*/'
      [b, a] = [st.pop(), st.pop()]
      switch t
        when '+' then st.push(a + b)
        when '-' then st.push(a - b)
        when '*' then st.push(a * b)
        when '/' then st.push(a / b)
      continue
    st.push(t)
  st[0]

to_s = (infix) -> infix.map((a) -> if 'object' == typeof a then "(#{to_s(a)})" else a).join('')

perm2rpn = (args, ops) ->
  [a, b, c, d] = args
  [X, Y, Z] = ops
  [
    [a, b, X, c, Y, d, Z]
    [a, b, X, c, d, Y, Z]
    [a, b, c, X, d, Y, Z]
    [a, b, c, X, Y, d, Z]
    [a, b, c, d, X, Y, Z]
  ].filter((a) -> Math.abs(evalRpn(a) - 24) < 1e-9)

perm2infix = (args, ops) -> perm2rpn(args, ops).map(rpn2infix).map(to_s)

merge = (a, b) -> b.map((x) -> [].concat(a, x))
perms = (arr) ->
  return [arr] if arr.length == 1
  [0...arr.length].reduce ((p, i) -> p.concat merge arr[i], perms arr[0...i].concat arr[(i + 1)...]), []

prod = (arr, n = 1) ->
  return arr.map((a) -> [a]) if n == 1
  arr.reduce ((p, b) -> p.concat merge b, prod(arr, n - 1)), []

equalTo24 = (a, b, c, d) ->
  opss = prod(['+', '-', '*', '/'], 3)
  cardss = perms([a, b, c, d])
  cardssObj = {}
  for cards in cardss
    cardssObj[cards.join('_')] = cards
  for cards in Object.values(cardssObj)
    for o in opss
      for res in perm2infix(cards, o)
        return res if Math.abs(eval(res) - 24) < 1e-9
  "It's not possible!"
_____________________________________________
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
ops =
  '+': (a,b)->a+b
  '-': (a,b)->a-b
  '*': (a,b)->a*b
  '/': (a,b)->a/b

equalTo24 = (u...) ->
  ns = permutes u
  for u in ns
    for o1, f1 of ops
      for i in [0..2]
        v = u[...i].concat [f1 u[i],u[i+1]].concat u[i+2..]
        for o2, f2 of ops
          for j in [0..1]
            w = v[...j].concat [f2 v[j],v[j+1]].concat v[j+2..]
            for o3, f3 of ops
              r = f3 w[0],w[1]
              if 1e-12 > Math.abs r-24
                v = u[...i].concat ["(#{u[i]}#{o1}#{u[i+1]})"].concat u[i+2..]
                w = v[...j].concat ["(#{v[j]}#{o2}#{v[j+1]})"].concat v[j+2..]
                return "#{w[0]}#{o3}#{w[1]}"
  "It's not possible!"
