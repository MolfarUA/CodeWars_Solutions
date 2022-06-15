local function isPrime(n)
  if n <= 2 or n % 2 == 0 then return n == 2 end
  for d = 3, n ^ 0.5, 2 do
    if n % d == 0 then return false end
  end
  return true
end

local function countEvenDigits(n)
  local r = 0
  while n > 0 do
    if n % 2 == 0 then r = r + 1 end
    n = n // 10
  end
  return r
end

local function f(n)
  local max = #tostring(n) - 1 - (tostring(n):sub(1, 1) == '1' and 1 or 0)
  local e, r = 0, 0
  for p = n - 1 - n % 2, 2, -2 do
    if isPrime(p) then
      local k = countEvenDigits(p)
      if k == max then return p end
      if k > e then
        e, r = k, p
      end
    end
  end
  return r
end

return f
____________________________________________
local function maximum(fn, iterator, iterand, key)
    local arg, value
    key, arg = iterator(iterand, key)
    value = fn(arg)
    local maxarg, maxvalue, maxkey = arg, value, key
    for key, arg in iterator, iterand, key do
        value = fn(arg)
        if value >= maxvalue then
            maxvalue = value
            maxarg = arg
            maxkey = key
        end
    end
    return maxkey, maxarg, maxvalue
end

local function nextdigit(b, n)
    if n > 0 then
        local x = n % b
        n = n // b
        return n, x
    end
end

local function eachdigit(n, base)
    return nextdigit, math.tointeger(base) or 10, math.tointeger(n)
end

local function count(predicate, ...)
    local result = 0
    for _, value in ... do
        if predicate(value) then
            result = result + 1
        end
    end
    return result
end

local function iseven(n)
    return n & 1 == 0
end

local function countevendigits(x)
    return count(iseven, eachdigit(x))
end

local cache = { false }

local function nextprime(max, prime)
    repeat prime = prime + 1 until cache[prime] or prime >= max
    if prime < max then return prime, prime end
end

local function primesbelow(max)
    if max - 1 > #cache then
        for i = #cache + 1, max - 1 do cache[i] = true end
        local prime = 2
        while prime <= #cache do
            for composite = prime * prime, #cache, prime do
                cache[composite] = false
            end
            repeat prime = prime + 1 until cache[prime] or prime > #cache
        end
    end
    return nextprime, max, 1
end

return function (n)
    return select(2, maximum(countevendigits, primesbelow(n)))
end
