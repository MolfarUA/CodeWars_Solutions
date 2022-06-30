53af2b8861023f1d88000832



areYouPlayingBanjo = (name) ->
  if name[0].toLowerCase() == "r"
    "#{name} plays banjo"
  else
    "#{name} does not play banjo"
________________________________
areYouPlayingBanjo = (name) ->
  if name[0].toLowerCase() == 'r'
    name + ' plays banjo'
  else
    name + ' does not play banjo'
________________________________
areYouPlayingBanjo = (name) ->
  name + if name[0] == 'R' or name[0] == 'r' then ' plays banjo' else ' does not play banjo'
________________________________
areYouPlayingBanjo = (name) -> "#{name} #{if name[0] in "rR" then "plays" else "does not play"} banjo"
