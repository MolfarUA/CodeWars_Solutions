57cfdf34902f6ba3d300001e


twoSort = (s) -> 
  s.sort()[0].split('').join('***')
___________________________
twoSort = (a) -> [a.sort()[0]...].join"***"
___________________________
twoSort = (s) -> [s.sort()[0]...].join('***')
___________________________
twoSort = (s) ->
  if s.length == 0 then '' else s.sort()[0].split('').join('***')
