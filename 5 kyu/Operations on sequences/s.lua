local solution = {}

function solution.solve(arr)
  local a = arr[1]
  local b = arr[2]
  local i = 1
  local lim = #arr // 2
  while (i < lim) do
    local x = a
    local y = b 
    local z = arr[2 * i + 1]
    local t = arr[2 * i + 2]
    a = math.abs(x * z - y * t)
    b = math.abs(x * t + y * z)
    i = i + 1
  end
  return {a, b}
end
return solution
_____________________________________
local solution = {}

-- return a table of 2 integers
function solution.solve(arr)
  local x, y = arr[1], arr[2]
  for i = 3, #arr, 2 do
    local a, b = arr[i], arr[i + 1]
    x, y = x * a - y * b, x * b + y * a
  end
  return {math.abs(x), math.abs(y)}
end
return solution
_____________________________________
local solution = {}

function solution.solve (array)
    local p = 1
    for i = 1, #array, 2 do
        p = p * (array[i]^2 + array[i+1]^2)
    end
  
    local a = 0
    while true do
        local b = math.sqrt(p - a^2)
        if b // 1 == b then return {a, b} end
        a = a + 1
    end
end

return solution
_____________________________________
function factorize(a, b, c, d)
    -- https://en.wikipedia.org/wiki/Brahmagupta%E2%80%93Fibonacci_identity
    return math.abs(a*c - b*d), math.abs(a*d + b*c)
end
local solution = {}

function solution.solve(arr)
    local i = 1
    local arr_n = #arr
    while arr_n >= 4 do
        local new_a, new_b = factorize(arr[arr_n-3], arr[arr_n-2], arr[arr_n-1], arr[arr_n])
        arr[arr_n-3] = new_a
        arr[arr_n-2] = new_b
        table.remove(arr, arr_n)
        table.remove(arr, arr_n-1)
        arr_n = arr_n - 2
    end
    return {arr[1], arr[2]}
end

return solution
