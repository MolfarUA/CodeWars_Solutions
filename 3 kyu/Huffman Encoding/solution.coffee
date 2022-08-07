54cf7f926b85dcc4e2000d9d



# takes: String; returns: [ [String,Int] ] (Strings in return value are single characters)
frequencies = (s)->
  hash = {}
  for ch in s
    hash[ch] ?= 0
    hash[ch]++
  kv_list = []
  for k,v of hash
    kv_list.push [k,v]
  kv_list.sort (a,b)->-(a[1]-b[1])
  kv_list

freqs2tree = (freqs)->
  # freq tree
  freqs = freqs.slice()
  while freqs.length > 1
    f2 = freqs.pop()
    f1 = freqs.pop()
    freqs.push [[f1, f2], f1[1]+f2[1]]
    # not optimal, should use log(T) algo
    freqs.sort (a,b)->-(a[1]-b[1])
  root = freqs[0]
  # code
  encode_hash = {}
  walk = (root, prefix)->
    if root[0] instanceof Array
      walk root[0][0], prefix+"0"
      walk root[0][1], prefix+"1"
    else
      encode_hash[root[0]] = prefix
    return
  if root
    walk root, ""
  {
    encode_hash
    decode_tree : root
  }

# takes: [ [String,Int] ], String; returns: String (with "0" and "1")
encode = (freqs,s)->
  return null if freqs.length <= 1
  {encode_hash} = freqs2tree freqs
  ret = []
  for ch in s
    ret.push encode_hash[ch]
  ret.join ""

# takes [ [String, Int] ], String (with "0" and "1"); returns: String
decode = (freqs,bits)->
  return null if freqs.length <= 1
  {decode_tree} = freqs2tree freqs
  ret = []
  tree = decode_tree
  for bit in bits
    tree = tree[0][bit]
    continue if tree[0] instanceof Array
    ret.push tree[0]
    tree = decode_tree
  ret.join ""

___________________________________________________
frequencies = (s)->
  fs = {}
  for c in s
    fs[c]?=0
    ++fs[c]
  [k,v] for k,v of fs

map = (fs,u)->
  t=fs[..]
  while t.length>1
    t.sort (a,b)->b[1]-a[1]
    a=t.pop()
    b=t.pop()
    t.push [[a[0],b[0]],a[1]+b[1]]
  q=[['',t[0][0]]]
  o={}
  while q.length
    [k,ab]=q.pop()
    for v,i in ab
      if Array.isArray v then q.push [k+i,v]
      else if u then o[k+i]=v else o[v]=k+i
  o

encode = (fs, s)->
  return null if fs.length<2
  m=map fs
  (m[c] for c in s).join ''

decode = (fs, e)->
  return null if fs.length<2
  m=map fs, yes
  o=k=''
  for c in e when m[k+=c]?
    o+=m[k]
    k=''
  o
