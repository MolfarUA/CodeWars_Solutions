55aa075506463dac6600010d


local solution = {}

function solution.listSquared(m, n)
  arr = {}
  for i=m,n do
    sum = 0
    for _,d in ipairs(divisors(i)) do sum = sum + d^2 end
    if math.sqrt(sum) == math.floor(math.sqrt(sum)) then
      table.insert(arr, {i, sum})
    end
  end
  return arr
end

function divisors(num)
  divs, ret = {}, {}
  for i=1,math.floor(math.sqrt(num)) do
    if num%i == 0 then
      divs[i] = 1
      divs[math.floor(num/i)] = 1
    end
  end
  for d,_ in pairs(divs) do table.insert(ret, d) end
  table.sort(ret)
  return ret
end

return solution
________________________________
local solution = {}

function solution.listSquared(m, n)
  local s, i = {}, m
  while i <= n do
    local sum, j = 0, 1
    while j * j <= i do
        if (i % j == 0) then
            sum = sum + j * j;
            local q = i // j
            if j ~= q then sum = sum + q * q end
        end
        j = j + 1
    end
    local sq = math.floor(math.sqrt(sum))
    if sq * sq == sum then
        table.insert(s, {i, sum})
    end
    i = i + 1
  end
  return s
end

return solution
________________________________
local solution = {}

function solution.listSquared(m, n)
  ret = {}
  for i = m, n do
    sq_divs = {}
    for j = 1, math.sqrt(i) do
      if i%j == 0 then
        if j == i//j then
          table.insert(sq_divs, j*j)
        else
          table.insert(sq_divs, j*j)
          table.insert(sq_divs, (i//j) * (i//j))
        end
      end
    end
      s = 0
      for j = 1, #sq_divs do
        s = s + sq_divs[j]
      end
      if math.sqrt(s) == math.floor(math.sqrt(s)) then table.insert(ret, {i, s}) end
  end
  return ret
end
return solution
