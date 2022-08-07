52597aa56021e91c93000cb0


moveZeros = (arr) ->
  (arr.filter (num) -> num isnt 0).concat(arr.filter (num) -> num is 0)
_____________________________
moveZeros = (arr) ->
  a = (i for i in arr when i isnt 0)
  a.push i for i in arr when i is 0
  a
_____________________________
moveZeros = (arr) ->
  i = 0
  len = arr.length
  
  for value in arr
    if value isnt 0
      arr[i++] = value
  
  while i < len
    arr[i++] = 0
  
  return arr
