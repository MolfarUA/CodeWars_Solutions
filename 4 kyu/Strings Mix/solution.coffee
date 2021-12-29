comp = (a, b) ->
  cp = b.length - a.length
  if cp == 0
    if a < b
      r = -1
    else
      r = 1
  else
    r = cp
  r

mix = (s1, s2) ->
  alpha_s1 = Array(27).join(1).split('').map(->
    0
  )
  alpha_s2 = Array(27).join(1).split('').map(->
    0
  )
  l1 = s1.length
  l2 = s2.length
  res = ''
  i = 0
  while i < l1
    c = s1.charCodeAt(i)
    if c >= 97 and c <= 122
      alpha_s1[c - 97]++
    i++
  i = 0
  while i < l2
    c = s2.charCodeAt(i)
    if c >= 97 and c <= 122
      alpha_s2[c - 97]++
    i++
  i = 0
  while i < 26
    sm = Math.max(alpha_s1[i], alpha_s2[i])
    if sm > 1
      if sm > alpha_s1[i]
        res += '2:' + Array(sm + 1).join(String.fromCharCode(i + 97)) + '/'
      else
        if sm > alpha_s2[i]
          res += '1:' + Array(sm + 1).join(String.fromCharCode(i + 97)) + '/'
        else
          res += '=:' + Array(sm + 1).join(String.fromCharCode(i + 97)) + '/'
    i++
  if res.length == 0
    return ''
  res.substring(0, res.length - 1).split('/').sort(comp).join '/'

__________________________________________________
mix = (s1, s2) ->
  [f1,f2]=f=[{},{}]
  for s,i in [s1,s2]
    for c in s when c isnt c.toUpperCase()
      f[i][c]?=0
      ++f[i][c]
  (for c in Array.from new Set Object.keys(f1).concat(Object.keys f2) when f1[c]>1 or f2[c]>1
    l=f1[c] ?0
    r=f2[c] ?0
    ['=1'[+(l>r)],'2'][+(l<r)] + ':' + Array(1+Math.max l,r).join c
  ).sort((a,b)->
    b.length-a.length or [1,-1][+(a<b)]
  ).join '/'

__________________________________________________
String.prototype.repeat = (count)->
  res = new Array count+1
  res.join @

mix = (s1, s2) ->
  hash = {}
  for ch in s1
    continue if !/[a-z]/.test ch
    hash[ch] ?= {
      ch
      count_1 : 0
      count_2 : 0
    }
    hash[ch].count_1++
  
  for ch in s2
    continue if !/[a-z]/.test ch
    hash[ch] ?= {
      ch
      count_1 : 0
      count_2 : 0
    }
    hash[ch].count_2++
  
  max_val = 0
  count_to_list_hash = {}
  for k,v of hash
    count = Math.max v.count_1, v.count_2
    count_to_list_hash[count] ?= []
    count_to_list_hash[count].push v
    max_val = Math.max max_val, count
  
  res_list = []
  for i in [max_val .. 2] by -1
    continue if !list = count_to_list_hash[i]
    sub_list = []
    for v in list
      cmp = "="
      cmp = "1" if v.count_1 > v.count_2
      cmp = "2" if v.count_1 < v.count_2
      count = Math.max v.count_1, v.count_2
      
      sub_list.push "#{cmp}:#{v.ch.repeat count}"
    sub_list.sort()
    res_list.push sub_list.join "/"
  
  res_list.join "/"
  
__________________________________________________
mix = (s1, s2) ->
  [c1, c2] = [s1, s2].map (s) -> [s...].sort().join('').match(/([a-z])\1+/g) or []
  [c1..., c2...].sort()
    .filter (c, i, arr) -> c[0] isnt arr[++i]?[0]
    .map (c) -> "#{(c in c1) + 2 * (c in c2)}:#{c}"
    .sort (a, b) -> b.length - a.length || a.localeCompare b
    .join('/').replace /3/g, '='
