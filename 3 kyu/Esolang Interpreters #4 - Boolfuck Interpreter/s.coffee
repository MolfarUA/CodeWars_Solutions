5861487fdb20cff3ab000030


boolfuck = (l,i='')->
  i=[].concat(([].map.call i, (a)->('0000000'+a.charCodeAt().toString 2)[-8..].split('').reverse())...).map (a)->+a
  o=[];s=[];c=d=0
  j='[':1,']':-1
  while 0<=c<l.length
    a=1-2*b=l[c] in '<]'
    switch l[c]
      when ','     then s[d]=i.shift() ?0
      when ';'     then o.push s[d] ?0
      when '<','>' then d+=a
      when '+'     then s[d]=+!s[d]
      when '[',']' then if !b is !s[d]
          n=1
          n+=a*(j[l[c+=a]] ?0) while n
    ++c
  o=(o.join('').match(/.{1,8}/g) ?[]).map (a)->parseInt a.split('').reverse().join(''), 2
  String.fromCharCode o...
_____________________________
boolfuck = (code, input = "") ->
  out = ""; stk = []; mem = {}; jmp = {};
  inp = [].concat([input...].map((c) -> [c.charCodeAt().toString(2).padStart(8, 0)...].reverse())...).map Number
  for i in [0...code.length]
    switch code[i]
      when "[" then stk.push i
      when "]" then jmp[i] = j = stk.pop(); jmp[j] = i
  idx = 0; ptr = 0
  while idx < code.length
    switch code[idx]
      when '>' then ptr++
      when '<' then ptr--
      when '+' then mem[ptr] ^= 1
      when ',' then mem[ptr] = inp.shift() ? 0
      when ';' then out += mem[ptr] ? 0
      when "[" then mem[ptr] or  (idx = jmp[idx])
      when "]" then mem[ptr] and (idx = jmp[idx])
    idx++;
  String.fromCharCode out.match(/.{1,8}/g).map((b) -> parseInt [b...].reverse().join"", 2)...
_____________________________
boolfuck = (code, tape = '') ->
  d={}
  L=[]
  t={'<':-1,'>':1}
  for i in [0..code.length-1]
    c=code[i]
    if c=='['
      L.push(i)
    else if c==']'
        a=L.pop()
        d[a]=i
        d[i]=a
      
      
  L=[0]
  s=''
  l=code.length
  i=p=0
  m=tape.split("").map((x)-> x.charCodeAt(0).toString(2).padStart(8,'0').split("").reverse().join("")).join("").split("").map(Number)
  while (i<l)
    c=code[i]
    if c=='>'
      p++
      L.push(0)
    else if c=='<'
        p--
        if p<0
          p++
          L.unshift(0)
    else if c=='+'
        L[p]^=1
    else if c==','
        L[p]= if m.length then m.shift() else 0
    else if c==';'
        s+=L[p]
    else if c=='[' && !L[p]
        i=d[i]
    else if c==']' && L[p]
        i=d[i]
    i++

  console.log((s+('0'.repeat(s.length%8))))
# console.log( (s+'0'.repeat(s.length%8)).match(/.{8}/g))
  return (s+('0'.repeat(s.length%8))).match(/.{8}/g).map((x)->String.fromCharCode(parseInt(x.split('').reverse().join(''),2))).join("")
