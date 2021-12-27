function doubleton(num::Integer)::Int
  while true
    num += 1
    length(Set(digits(num))) == 2 && return num
  end
end

##############
function doubleton(num::Integer)::Int
  num += 1
  while length(unique(digits(num))) != 2
    num += 1
  end
  num  
end

############
function doubleton(num::Integer)::Int
    while true
        num += 1
        if length(Set(digits(num)))==2
            return num
        end
    end
end

################
function doubleton(num::Integer)::Int
  num += 1
  while length(unique(digits(num))) ≠ 2
    num += 1
  end
  num
end

###############
function doubleton(num::Integer)::Int
  length(unique(digits(num+1))) == 2 ? num+1 : doubleton(num+1)
end
