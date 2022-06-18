add = (a, b) -> a + b

findEvenIndex = (arr) ->
  arr.findIndex (num, i, a) -> a.slice(0, i).reduce(add, 0) == a.slice(i + 1).reduce(add, 0)
________________________
findEvenIndex = (arr) ->
  for i in [0..arr.length]
    if arr.slice(0, i).reduce(((sum, a) -> sum + a), 0) == arr.slice(i + 1).reduce(((sum, a) => sum + a), 0)
      return i
  return -1
________________________
findEvenIndex = (arr) ->
  r = arr.reduce((a, b) => a + b)
  l = 0

  for v, i in arr
    r -= v

    if (l == r)
      return i

    l += v
  -1
________________________
summ = (arr) -> arr.reduce ((total, a) -> total + a), 0

findEvenIndex = (arr) ->
  for i in [0...arr.length] by 1
    arrA = arr[0...i]
    arrB = arr[i+1...arr.length]
    if summ(arrA) == summ(arrB)
      return i
  return -1 
________________________
findEvenIndex = (arr) ->
  n = arr.length
  i = 0
  while i < n
    leftsum = 0
    rightsum = 0
    j = 0
    while j < i
      leftsum += arr[j]
      j++
    j = i + 1
    while j < n
      rightsum += arr[j]
      j++
    if leftsum == rightsum
      return i
    ++i
  -1
