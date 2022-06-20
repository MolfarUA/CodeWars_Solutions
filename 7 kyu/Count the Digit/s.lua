566fc12495810954b1000030


local solution = {}

function solution.nbDig(n, d)
    -- your code
  local nums={}
  local result=0
  for i=0,n do
    local _,t=tostring(i*i):gsub(d,"")
    result=result+t
  end
    return result
end
  
return solution
____________________________
local solution = {}

function solution.nbDig(n, d)
  local ret, sd = 0, tostring(d)
  for i=0,n do
    for x in string.gmatch(tostring(i*i), '.') do
      if x == sd then ret = ret + 1 end
    end
  end
  return ret
end

return solution
____________________________
local solution = {}

function solution.nbDig(n, d)
    local result = 0
    while n >= 0 do
        local k = n * n
        while k ~= 0 do
            if k % 10 == d then result = result + 1 end
            k = k // 10
        end
        n = n - 1
    end
    if (d == 0) then result = result + 1 end
    return result
end

return solution
