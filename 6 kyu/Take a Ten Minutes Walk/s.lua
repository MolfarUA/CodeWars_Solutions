return {
  is_valid_walk = function(walk)
    if #walk ~= 10 then return false end
    pos = {0, 0}
    for i, direction in ipairs(walk) do
      if direction == 'n' then pos[2] = pos[2] + 1 end
      if direction == 's' then pos[2] = pos[2] - 1 end
      if direction == 'w' then pos[1] = pos[1] - 1 end
      if direction == 'e' then pos[1] = pos[1] + 1 end 
    end
    return pos[1] == 0 and pos[2] == 0
  end
}
__________________________________________
return {
  is_valid_walk = function(walk)
    local s = table.concat(walk)
    local function count(x) return select(2, s:gsub(x, '')) end
    return #s == 10 and count('n') == count('s') and count('w') == count('e')
  end
}
__________________________________________
return {
  is_valid_walk = function(walk)
    if #walk ~= 10 then return false end
    
    local dir_table = {n=0,e=0,s=0,w=0}
    for index, dir in ipairs(walk) do
      dir_table[dir] = dir_table[dir] + 1
    end
    
    return dir_table['n'] == dir_table['s'] and dir_table['e'] == dir_table['w']
  end
}
__________________________________________
return {
  is_valid_walk = function(walk)
    c={}
    cont=0
    for i=1,#walk do
      print(walk[i])
      if(walk[i]=='n') then
        c['n']= (c['n'] or 0 )+1
      elseif(walk[i]=='s') then
        c['s']= (c['s'] or 0)+1
      elseif(walk[i]=='e') then
        c['e']= (c['e'] or 0)+1
      elseif(walk[i]=='w') then
        c['w']= (c['w'] or 0)+1
      end
      cont=cont+1
    end
    
    if ((c['n']==c['s']) and (c['e']==c['w']) and(cont==10)) then
      return true
    else
      return false
    end
  end
}
