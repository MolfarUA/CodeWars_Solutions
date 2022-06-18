544675c6f971f7399a000e79


local kata = {
  string_to_number = tonumber
}

return kata
_______________________
return { string_to_number = tonumber }
_______________________
local kata = {}

function kata.string_to_number(s)
  return tonumber(s)
end

return kata
_______________________
local kata = {}

function kata.string_to_number(s)
  return s - '0'
end

return kata
_______________________
local kata = {}

function kata.string_to_number(s)
  return tonumber(s, 10);
end

return kata
_______________________
local kata = {}

function kata.string_to_number(s)
  if s == nil then
    return s
  end
  local bFu = false
  
  local nRet = 0;
  for i = 1, string.len(s) do
    repeat
      if i == 1 and string.sub(s, 1, 1) == '-' then
        bFu = true
        break
      end

      nRet = nRet * 10 + (string.byte(s, i) - string.byte(0));
    until true
  end
  
  return (bFu and -nRet or nRet)
end

return kata
