local solution = {}

--- convert number into bin
-- @return bin number as string
function toBin(number)
        local bin = {}

        if number == 0 then
                return '0'
        elseif number == 1 then
                return '1'
        end
        while number ~= 0 do
                bin[#bin+1]=number%2
                number=math.floor(number/2)
        end
        return table.concat(bin):reverse()
end

--- code string with numbers
--  @return coded string
function solution.code(str)
        local result = {}
        for i=1, #str do
                local num = tonumber(str:sub(i, i))
                local bits = math.ceil(math.log(num+1)/math.log(2))
                local num_code = ""
                for j=1, bits-1 do
                        num_code=num_code..'0'
                end
                num_code=num_code..'1'..toBin(num)
                result[i] = num_code
        end
        return table.concat(result)
end

function solution.decode(str)
        local result = {}
        local block = ""
        local i = 1
        while i < #str do
                local num = str:sub(i, i)
                block=block..num
                if tonumber(num) == 1 then
                        local bits = #block-1
                        i=i+1
                        local number = tonumber(str:sub(i, i+bits), 2)
                        result[#result+1] = number
                        print(block..' '..str:sub(i, i+bits)..": "..tostring(number))
                        i=i+bits+1
                        block=""
                else
                        i=i+1
                end
        end
        return table.concat(result)
end

return solution
__________________________
local solution = {}

local function toBits(number)
    if number == 0 then return 0 end
    local result = ""
    local d, m = number, 0
    while d ~= 0 do
        m = d%2
        d = d//2
        result = result..tostring(math.floor(m))
    end
    return string.reverse(result)
end

function solution.code(s)
    local result = ""
    for i = 1, #s do
        local bits = toBits(string.sub(s, i, i))
        local k = #bits
        local part = ""
        for i = 1, k-1 do 
            part = part.."0"
        end
        part = part.."1"..bits
        result = result..part
    end
    return result 
end

function solution.decode(str)
    local result = ""
    local remain = string.sub(str, 1, #str)
    while #remain ~= 0 do
        for i = 1, #remain do
            if string.sub(remain, i, i) == "1" then
                local len = i
                local currStr = string.sub(remain, i+1, i+len)
                result = result..tostring(tonumber(currStr, 2))
                remain = string.sub(remain, i+len+1, #remain)
                break
            end
        end
    end
    return result
end

return solution
__________________________
local solution = {}

local code = {
  ["0"] = "10", ["1"] = "11",
  ["2"] = "0110", ["3"] = "0111",
  ["4"] = "001100", ["5"] = "001101",
  ["6"] = "001110", ["7"] = "001111",
  ["8"] = "00011000", ["9"] = "00011001"
}

function solution.code(s)
    local result = ""
    for i = 1, s:len() do
        result = result .. code[s:sub(i,i)]
    end
    return result
end

function solution.decode(str)
    local i, j = 0, 0
    local result = ""
    repeat i, j = str:match("()0*1()", i)
        if i then
            i = j + j - i
            result = result .. tonumber(str:sub(j, i - 1), 2)
        end
    until not i
    return result
end

return solution
__________________________
local solution = {}
-- function solution.code(s)
--     local m, res = {'10','11','0110','0111','001100','001101','001110','001111','00011000','00011001'}, ""
--     for i = 1, #s do
--       local v = m[tonumber(string.sub(s, i, i)) + 1]
--       res = res .. v
--     end
--     return res 
-- end

function ten2two(s,sn)
  if s~=1 and s~=0 then return ten2two(s//2,(math.floor(s%2))..sn) 
  else return math.floor(s)..sn
  end
end


function solution.code(s)
    -- your code
--   s="0"
  local str_list={}
  s:gsub(".",function(c) table.insert(str_list,c) end)
  local code_list={}
  local result=""
  for i=1,#str_list do
    if str_list[i]=="0" then result=result.."10" 
    elseif str_list[i]=="1" then result=result.."11"
    else
      local ch=ten2two(str_list[i],"")
      result=result..string.rep("0",tonumber(#ch)-1).."1"..ch
    end
--     table.insert(code_list,ten2two(str_list,""))
  end
    return result
end

function solution.decode(str)
--   local str_list={}
--   local n=0
--   local save={}
--   str:gsub(".",function(c) table.insert(save,c) end)
--   for i=1,#str do
--     n=n+1
--     if save[i]==1 then
      
-- --   for k,v in str:gmatch("[1+]")do
-- --   table.insert(str_list,{k,v})
-- --   end
-- --   ss=string.find(str,'[^'.."1+"..']+',1)
-- --   for i=1,#str do
    
  
--     -- your code
--     return str_list
    local ret, i, lg = "", 1, #str
    while (i <= lg) do
        local zero_i = i
        while zero_i <= lg and string.sub(str, zero_i, zero_i) ~= "1" do
            zero_i = zero_i + 1--
        end
        local l = zero_i - i + 2
        local ss = string.sub(str, zero_i + 1, zero_i + l - 1)
        ret = ret .. tonumber(ss, 2)
        i = zero_i + l
    end
    return ret
end

return solution
