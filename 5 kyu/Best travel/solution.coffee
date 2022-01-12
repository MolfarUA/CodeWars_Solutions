chooseBestSum = (t, k, ls) ->
  m = 0
  walk = (xs, j) ->
    if xs.length == k
      n = xs.reduce(((a, b) ->
        a + b
      ), 0)
      if n > m and n <= t
        m = n
    else
      i = j + 1
      while i < ls.length
        walk xs.concat(ls[i]), i
        i++
    return
  walk [], -1, 0, ls
  if m == 0 then null else m
_______________________________________
comb = (ls, k) ->
  i = undefined
  sub1 = undefined
  res = []
  subset = undefined
  nxt = undefined
  i = 0
  while i < ls.length
    if k == 1
      res.push [ ls[i] ]
    else
      subset = comb(ls.slice(i + 1, ls.length), k - 1)
      sub1 = 0
      while sub1 < subset.length
        nxt = subset[sub1]
        nxt.unshift ls[i]
        res.push nxt
        sub1++
    i++
  res

chooseBestSum = (t, k, ls) ->
  a = comb(ls, k)
  mx = -1
  res = []
  i = 0
  while i < a.length
    s = a[i].reduce((a, b) ->
      a + b
    )
    if s >= mx and s <= t
      res = [
        a[i]
        s
      ]
      mx = s
    i++
  if res.length != 0 then res[1] else null
_______________________________________
chooseBestSum = (t, k, ls) ->
  comb = (t, k, ls, i) ->
    if k == 0 and t >= 0
      return 0
    if k < 0 or i >= ls.length
      return -Infinity
    Math.max comb(t, k, ls, i + 1), ls[i] + comb(t - (ls[i]), k - 1, ls, i + 1)
  r = comb(t, k, ls, 0)
  if r < 0 then null else r
_______________________________________
chooseBestSum = (t, k, ls) ->
  maxi = -Infinity
  for i in [0...2 ** ls.length]
    arr = []
    for j in [0...ls.length]
      if i & (2 ** j)
        arr.push(ls[j])   
    if arr.length == k
      n = arr.reduce(((a, b) -> a + b), 0)
      if n > maxi && n <= t
        maxi = n 
  if maxi == -Infinity then null else maxi
_______________________________________
chooseBestSum = (limit, count, list) ->
  return null if list.length < count
  list = list.slice()
  list.sort (a,b)->a-b
  
  val_list = list.slice(0, count)
  base_set = {
    val_list
    idx_list : [0 ... count]
    sum      : val_list.reduce (a,b)->a+b
  }
  uniq_hash = {}
  uniq_hash[base_set.idx_list.join()] = true
  best = base_set
  unchecked_set_list = [base_set]
  
  len = list.length
  while unchecked_set_list.length
    new_unchecked_set_list = []
    for set in unchecked_set_list
      for replace_pos in [0 ... count]
        idx = set.idx_list[replace_pos]
        for new_idx in [idx+1 ... len] by 1
          continue if -1 != set.idx_list.indexOf new_idx
          mod_set = {
            val_list : []
            idx_list : []
            sum      : 0
          }

          sum = 0
          insert_done = false
          last_idx = 0
          for i in [0 ... count]
            insert_idx = set.idx_list[i]
            if i > replace_pos and !insert_done and insert_idx > new_idx
              sum += val = list[new_idx]
              mod_set.val_list.push val
              mod_set.idx_list.push new_idx
              insert_done = true
            if i != replace_pos
              sum += val = set.val_list[i]
              mod_set.val_list.push val
              mod_set.idx_list.push set.idx_list[i]
          
          if !insert_done
            sum += val = list[new_idx]
            mod_set.val_list.push val
            mod_set.idx_list.push last_idx = new_idx
          
          mod_set.sum = sum
          break if sum > limit
          key = mod_set.idx_list.join()
          continue if uniq_hash[key]
          uniq_hash[key] = true

          best = mod_set if best.sum < sum

          new_unchecked_set_list.push mod_set
      
    unchecked_set_list = new_unchecked_set_list
  
  if best.sum <= limit
    best.sum
  else
    null
