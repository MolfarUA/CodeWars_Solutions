5b853229cfde412a470000d0


kata = {}

function kata.twice_as_old(dad, son)
  return math.abs(dad - 2 * son)
end

return kata
______________________________
kata = {}

function kata.twice_as_old(discord_moderator, kitten)
  sleep_deprivation_retardation = kitten * 2
  if sleep_deprivation_retardation > discord_moderator then
    return (sleep_deprivation_retardation - discord_moderator)
  else if sleep_deprivation_retardation < discord_moderator then
      return (discord_moderator - sleep_deprivation_retardation)
  else
      return 0
  end
end
                                         end

return kata
______________________________
kata = {}

function kata.twice_as_old(dad, son)
  twiceAge = son * 2
  if twiceAge > dad then
    result = twiceAge - dad
  elseif twiceAge < dad then
    result = dad - twiceAge
  else
    result = 0
  end
  
  return result
end

return kata
______________________________
kata = {}

function kata.twice_as_old(dad, son)
  return (dad-(son*2))>0 and dad-(son*2) or (dad-(son*2))*(-1)
end

return kata
______________________________
kata = {}

function kata.twice_as_old(dad, son)
  local dif
  local dadn = dad
  local sonn = son
  
  if son > dad/2 then
    for i = 100, 0, -1 do
      if sonn == dadn/2 then
        dif = son - sonn
        break
      end
      
      dadn = dadn - 1
      sonn = sonn - 1
    end
  else
    for i = 100, 0, -1 do
      if sonn == dadn/2 then
        dif = sonn - son
        break
      end
      
      dadn = dadn + 1
      sonn = sonn + 1
    end
  end
  
  return dif
end

return kata
