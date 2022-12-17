5844a422cbd2279a0c000281


multi = (arr) ->
  arr.reduce(((a, b) -> a * b), 1)

add = (arr) ->
  arr.reduce(((a, b) -> a + b), 0)
  
reverse = (str) ->
  [str...].reverse().join("")
________________________
multi = (arr) ->
  arr.reduce((a, b) => a * b)
  
add = (arr) ->
  arr.reduce((a, b) => a + b)
  
reverse = (str) ->
  str.split('').reverse().join('')
________________________
multi = (arr) ->
  answer = 1
  i = 0
  while i < arr.length
    answer *= arr[i]
    i++
  answer

add = (arr) ->
  answer = 0
  i = 0
  while i < arr.length
    answer += arr[i]
    i++
  answer

reverse = (str) ->
  str.split('').reverse().join ''
