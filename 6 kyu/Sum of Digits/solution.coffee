digital_root = (n) ->
  --n % 9 + 1
  
________________________________
digital_root = (n)->
  if n>0 then 1 + ((parseInt(n) - 1) % 9) else 0
    
________________________________
digital_root = (n) -> 1 + (n - 1) % 9

________________________________
digital_root = (n)->
  if "#{n}".length > 1
    result = eval("#{n}".replace(/(\d)(?=\d)/g, '$1+'))
    digital_root(result)
  else
    n
    
________________________________
digital_root = (n)->
  while n > 9
    n = String(n).split("").reduce ((prev, value) -> prev + +value), 0
  n
  
________________________________
digital_root = (n)->
  return --n % 9 + 1

________________________________
digital_root = (num) ->
  num = num.toString()
  if num.length is 1
    return +num
  if(num.length > 1)
    nnum = num.split('').reduce((a,b) -> +a + +b)
    return digital_root(nnum)
