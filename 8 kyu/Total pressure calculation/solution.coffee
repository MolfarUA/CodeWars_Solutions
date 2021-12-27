doubleton = (num) -> 
  while (true)
    num++
    if (new Set(String(num)).size == 2)
      return num

____________________
doubleton = (num) ->
  num++
  until new Set(num.toString()).size == 2
    num++
  num
_____________________
doubleton = (num) ->
  num++
  while new Set(num.toString()).size != 2
    num++
  num
____________________
doubleton = (num) -> 
  digits=(n)->n.toString().split('').reduce(
    (digs,x)->
      if digs.indexOf(x)<0 then digs.push(x);
      digs
    ,[]);
  i=num+1
  while digits(i).length!=2
    i++
  i
_______________________
doubleton = (num) -> 
  set = new Set()
  while set.size isnt 2
    set = new Set()
    num++
    for char in num.toString()
      set.add(char)
  num
______________________
doubleton = (n) ->
  while new Set(++n + '').size != 2
    continue
  n
______________
doubleton = (num) -> 
  num += 1
  while(new Set(''+num).size != 2)
    num++
  return num
