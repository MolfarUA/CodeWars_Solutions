function order(words)
    local function split(inputstr, sep)
        if sep == nil then
                sep = "%s"
        end
    
        local t={}
        for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
                table.insert(t, str)
        end
        return t
    end
  
    local tbl = split(words, " ")
    local pos_tbl = {}
  
    local r = ""
  
    for _, v in ipairs(tbl) do
        for i=0, string.len(v) do
            local t = tonumber(string.sub(v, i, i))
      
            if t then
                pos_tbl[t] = v
            end
        end
    end
  
    for k, v in ipairs(pos_tbl) do
        if k > 1 then
            r = r.." "
        end
    
        r = r..v
    end
  
    return r
end

_____________________________________________
function order(words)
  local str = ""
  local tab = {} 
  for i=1,#words do
    if words:sub(i, i) == " " and str ~= "" then
      tab[#tab + 1] = str
      str = ""
    else
      str = str .. words:sub(i, i)
    end
  end
  if str ~= "" then
    tab[#tab + 1] = str
  end
  local continue
  local outtab = {}
  for i=1,#tab do
    continue = true
    for j=1,#tab[i] do
      if tonumber(tab[i]:sub(j, j)) then
        outtab[tonumber(tab[i]:sub(j, j))] = tab[i]
      end
    end
  end
  return table.concat(outtab, " ")
end

_____________________________________________
function order(words)
  -- ...
  local arr = {}
  for w in string.gmatch(words, "%S+") do
    table.insert(arr,w)
  end
  local res = {}
  for k,v in pairs(arr) do
    local t;
    for i=1,string.len(v) do
      local num = tonumber(string.sub(v,i,i))
      if num then t = num end
    end
    table.insert(res,{x = t,y = v})
  end
  table.sort(res,function(a,b) 
      return (a.x < b.x)
  end)
  local ans = ""
  for k,v in pairs(res) do
    ans = ans .. v.y .. " ";  
  end
  return string.sub(ans,1,#ans-1)
end

_____________________________________________
function order(words)
  
  local result = {}

  for word in words:gmatch('%g+') do
      local num = tonumber(word:match('%d'))
      result[num] = word:gsub('%s', '')
  end
  
  return table.concat(result, ' ')
  
  
end

_____________________________________________
function order(words)
  if words == "" then return words end
  
  local orderedWords = {}
  local orderedString = ""
  
  for char in words:gmatch("%S+") do
    orderedWords[tonumber(string.match(char, "%d+"))] = char
  end
  
  for i = 1, #orderedWords do
    if i == #orderedWords then
      orderedString = orderedString .. orderedWords[i]
    else
      orderedString = orderedString .. orderedWords[i] .. " "
    end
  end
  return orderedString
end
