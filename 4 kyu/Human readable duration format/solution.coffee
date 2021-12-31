formatDuration = (seconds) ->
    return 'now' if seconds is 0
    ("#{value} #{unit}#{if value == 1 then '' else 's'}" for [value, unit] in [
        [seconds // 60 // 60 // 24 // 365, "year"]
        [seconds // 60 // 60 // 24 % 365, "day"]
        [seconds // 60 // 60 % 24, "hour"]
        [seconds // 60 % 60, "minute"]
        [seconds % 60, "second"]
        ] when value).join(', ').replace(/(.*), /, "$1 and ")
    
___________________________________________________
formatDuration = (t)->
  return 'now' unless t
  (for k,p of second:60,minute:60,hour:24,day:365,year:Infinity when (r=t%p;t//=p;r)
    "#{r} #{k}#{'s'[...r>1]}"
  ).reverse().reduce (s,t,i,a)->s+[' and ',', '][+(i<a.length-1)]+t

___________________________________________________
formatDuration = (seconds) ->
  UNITS = [
    [ 'year', 60 * 60 * 24 * 365 ]
    [ 'day', 60 * 60 * 24 ]
    [ 'hour', 60 * 60 ]
    [ 'minute', 60 ]
    [ 'second', 1 ]
  ]
  if seconds == 0
    'now'
  else
    parts = UNITS.reduce((memo, curr) ->
      n = Math.floor(seconds / curr[1])
      seconds %= curr[1]
      switch n
        when 0
          memo
        when 1
          memo.concat("1 #{curr[0]}")
        else
          memo.concat("#{n} #{curr[0]}s")
    , [])
    if parts.length == 1 then parts[0] else "#{parts[...-1].join(', ')} and #{parts[parts.length - 1]}"

___________________________________________________
formatDuration = (t)->
  return 'now' unless t
  (for k,p of second:60,minute:60,hour:24,day:365,year:Infinity when (r=t%p;t//=p;r)
    "#{r} #{k}#{'s'[1-(r>1)..]}"
  ).reverse().reduce (s,t,i,a)->s+[' and ',', '][+(i<a.length-1)]+t
