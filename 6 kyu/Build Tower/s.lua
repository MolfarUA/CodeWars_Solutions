576757b1df89ecf5bd00073b


function towerBuilder(floorCount)
  local tower = { }
  
  for i = 1, floorCount do
    local  air  = (' '):rep(floorCount - i)
    local floor = ('*'):rep(2 * i - 1)
    
    -- add floor surrounded by air
    tower[#tower + 1] = air .. floor .. air
  end
  
  return tower
end
_____________________________
function towerBuilder(nFloors)
  local table = {}
  for i = 0,(nFloors-1),1 do
    local odd_relation = ((2*i)+1)
    local max_odd_relation = (2*(nFloors-1))+1
    local star = string.rep("*",odd_relation)
    local space = max_odd_relation - odd_relation
    table[i+1] = string.rep(" ",(space/2))..star.. string.rep(" ",(space/2))
  end
  return table
end
_____________________________
function towerBuilder(nFloors)
  -- build here
  local s = {}
  for i = 1,nFloors do
    s[i] = string.rep(" ",nFloors-i) .. string.rep("*",i*2-1) .. string.rep(" ",nFloors-i)
  end
  return s
end
_____________________________
function towerBuilder(n)
  local s,r,t = string.rep("*", n+n-1), {}, 1
  for i = n,1,-1 do
    r[i] = s
    s = s:gsub("%*%s*$", string.rep(" ", t)):gsub("^%s*%*", string.rep(" ", t))
    t = t + 1
  end
  return r
end
_____________________________
function towerBuilder(nFloors)
tower = {}
space = " "
spaceNum = nFloors-2
star = 0
for i=1, nFloors do
  tower[i] = ""
  for y=0, spaceNum do
    tower[i] = tower[i].." "
  end
  for x=0, star do
    tower[i] = tower[i].."*"
  end
  for y=0, spaceNum do
    tower[i] = tower[i].." "
  end
  spaceNum = spaceNum - 1
  star = star + 2
end
return tower
end
_____________________________
function towerBuilder(nFloors)
  local result = {}
  for n = 1, nFloors do
    local spc = string.rep(" ", nFloors - n)
    local stars = string.rep("*", 2 * n - 1)
    table.insert(result, spc .. stars .. spc)
  end
  return result
end
