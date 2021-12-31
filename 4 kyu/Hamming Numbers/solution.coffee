hamming = (n) ->
  o = [1]
  i = j = k = 0
  while --n
    a = 2 * o[i]
    b = 3 * o[j]
    c = 5 * o[k]
    x = Math.min(a, b, c)
    o.push x
    if a is x then i++
    if b is x then j++
    if c is x then k++
  o.pop()
  
___________________________________________________
hamming = (n) ->
  i = 0
  j = 0
  k = 0
  h = [1]
  nl = 1
  while (n > 0)
    if (h[i]*2 <= nl) then i+=1
    if (h[j]*3 <= nl) then j+=1
    if (h[k]*5 <= nl) then k+=1
    nl = Math.min(h[i]*2, h[j]*3, h[k]*5)
    h.push(nl)
    n = n - 1
  h[h.length-2]
  
___________________________________________________
hamming = (n) ->
  xs = new Array(n)
  xs[0] = 1
  ai = 0
  bi = 0
  ci = 0
  a = 2
  b = 3
  c = 5
  i = 1
  while i < n
    xs[i] = Math.min(a, Math.min(b, c))
    if xs[i] == a
      a = 2 * xs[++ai]
    if xs[i] == b
      b = 3 * xs[++bi]
    if xs[i] == c
      c = 5 * xs[++ci]
    i++
  xs[n - 1]
  
___________________________________________________
H = [1]

i = j = k = 0
for n in [1...5000]
  if 2 * H[i] is H[n - 1] then i++
  if 3 * H[j] is H[n - 1] then j++
  if 5 * H[k] is H[n - 1] then k++
  H.push Math.min 2 * H[i], 3 * H[j], 5 * H[k]

hamming = (number) -> H[number - 1]
