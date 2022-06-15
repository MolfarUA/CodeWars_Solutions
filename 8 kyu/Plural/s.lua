function isPlural(n)
  return n ~= 1
end

return isPlural
__________________
function isPlural(n)
  return n == 0 or n > 1
end

return isPlural
__________________
function isPlural(n)
  if n > 1 then
    return true
  elseif n < 1 then
    return true
  elseif n == 1 then
    return false
  end
end

return isPlural
__________________
function isPlural(n)
  if n == 1 then return false end
  return true
end

return isPlural
__________________
function isPlural(n)
 if n > 1 or n == 0 then
  return true
    else
    return false
end
end
return isPlural
