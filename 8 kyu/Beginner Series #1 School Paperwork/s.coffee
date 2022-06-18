55f9b48403f6b87a7c0000bd


paperwork = (n, m) ->
  if m < 0 or n < 0 then 0 else m * n
__________________________
paperwork = (n, m) ->
  Math.max(n, 0) * Math.max(m, 0)
__________________________
paperwork = (n, m) ->
  if n < 0 or m < 0
    0
  else
    n * m
__________________________
paperwork = (n, m) ->
  if n>0 & m>0 then return n*m
  0
__________________________
paperwork = (n, m) -> if (n < 1 || m < 1) then 0 else (n * m)
__________________________
paperwork = (n, m) -> if n < 0 or m < 0 then 0 else n*m
__________________________
paperwork = (n, m) ->
  if(m > 0 && n > 0)
    return m*n;
  return 0;
