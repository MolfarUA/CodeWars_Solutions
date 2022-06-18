function digitize(str)
  local arr = {}
  for digit in string.gmatch(str, "%d") do
    table.insert(arr, digit)
    
  end
  
  local reversedTable = {}
  local itemCount = #arr
  local a = 0
  for k, v in ipairs(arr) do
       reversedTable[itemCount + 1 - k] = tonumber(v)
      a = v
   end
  return reversedTable

end

return digitize
________________________
function digitize(n)
  
 local t={}
 str=string.reverse(tostring(n))
 str:gsub(".",function(c) table.insert(t,tonumber(c)) end)

 return t
  
end

return digitize
________________________
function digitize(n)
  if n == 0 then return {0} end
  result = {}
  while (n > 0) do
    table.insert(result,n%10)
    n = n//10
  end
  return result
end

return digitize
________________________
function digitize(n)
  local res = {}
  for digit in string.gmatch(string.reverse(n),"%d") do
    res[#res+1] = tonumber(digit)
  end
  return res
end

return digitize
