local function ips_between(start, finish)
  local function IpToInteger(IP)
    local o1, o2, o3, o4 = IP:match("(%d+)%.(%d+)%.(%d+)%.(%d+)")
    return (o1 * 256^3) + (o2 * 256^2) + (o3 * 256) + o4
  end
  local StartIp = IpToInteger(start)
  local FinishIp = IpToInteger(finish)
  return FinishIp - StartIp
end

return ips_between
__________________
local function ipToNum(ip)
    local a, b, c, d = ip:match("(%d+)%.(%d+)%.(%d+)%.(%d+)")
    return tonumber(a) * 16777216 + tonumber(b) * 65536 + tonumber(c) * 256 + tonumber(d)
end

local function ips_between(start, finish)
    return ipToNum(finish) - ipToNum(start)
end

return ips_between
________________
local function GetValue(str)
   local result = 0
   
   local createdValue = ""
   local word = ""
  
   for i = 1, string.len(str) do
      local symbol = string.sub(str, i, i)
      
      if symbol ~= "." then
         word = word..symbol
      end
      
      if symbol == "." or i == string.len(str) then
         wordNumber = tonumber(word)
         convertedBinary = ""
      
         while wordNumber ~= 0 do
            convertedBinary = tostring(wordNumber % 2)..convertedBinary
            wordNumber = math.floor(wordNumber / 2)
         end
         
         if string.len(convertedBinary) ~= 8 then
            for i = 1, 8 - string.len(convertedBinary) do
               convertedBinary = "0"..convertedBinary
            end
         end
         
         createdValue = createdValue..convertedBinary
         word = ""
      end
   end
   
   for i = 1, 32 do
      local symbol = string.sub(createdValue, i, i)
      if symbol == "1" then
         result = result + 2^(32 - i)
      end
   end
   
   return math.floor(result)
end

local function ips_between(start, finish)
   return GetValue(finish) - GetValue(start)
end

return ips_between
