local kata = {}


function kata.number_of_pairs(gloves)
--My hands are freezing
    local t = {}
    local count = 0
    for k, v in ipairs(gloves) do
        if t[v] then
            count = count + 1
            t[v] = nil
        else
            t[v] = 1
        end
    end
    return count
end

return kata

______________________
local kata = {}


function kata.number_of_pairs(gloves)
--My hands are freezing
  local glovesTable = {};
  
  for k,v in ipairs(gloves) do
    glovesTable[v] = (glovesTable[v] or 0) + 1
  end
  
  local pairsSum = 0;
  for k,v in pairs(glovesTable) do
     pairsSum = pairsSum + v//2;
  end
  
  return pairsSum;
end

return kata

______________________
local kata = {}


function kata.number_of_pairs(gloves)
  local glove_hash = {}
  local glove_pairs = 0
  
  for i, v in pairs(gloves) do
    if glove_hash[v] then 
      glove_pairs = glove_pairs + 1 
      glove_hash[v] = nil
    else
      glove_hash[v] = v
    end
  end
  
  return glove_pairs
end

return kata

__________________________
local kata = {}

function kata.number_of_pairs(gloves)
  local t, s = {}, 0
  for _, v in ipairs(gloves) do t[v] = (t[v] or 0) + 1 end
  for _, v in pairs(t) do s = s + v // 2 end
  return s
end

return kata
