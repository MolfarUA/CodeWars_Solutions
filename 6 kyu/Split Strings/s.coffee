515de9ae9dcfc28eb6000001


solution = (str) ->
    str += '_' if str.length % 2 isnt 0
    (str[i] + str[i+1]) for s, i in str by 2
________________________________
solution = (str) ->
  (str + "_").match(/../g) || []
________________________________
solution = (str) -> str.split(/(..)/g).filter((x)->x).map((s) -> if s.length&1 then s+'_' else s)
________________________________
solution = (s) -> (s+'_').match(/(..)/g)||[]
________________________________
solution = (str) ->
  result = []
  i = 0
  while i < str.split('').length
    result.push str.slice(i, i + 2)
    i += 2
  if result.length > 0 and result[result.length - 1].length == 1
    result[result.length - 1] += '_'
  result
