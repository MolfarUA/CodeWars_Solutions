def doubleton(num)
  num.succ.step.find{ |i| i.digits.uniq.size == 2 }
end

#############
def doubleton(num)
  for i in (num+1)..1000000
    if i.to_s.chars.sort.join.squeeze.size == 2
      return i 
    end
  end
end

###################
def doubleton(num)
  (num+1..1000000).each do |num|
    return num if num.digits.uniq.size == 2
  end
end

##############
def doubleton(num)
  loop do
    num += 1
    return num if num.digits.uniq.size == 2
  end
end

################
def doubleton(num)
  answer = num + 1
  answer += 1 while answer.digits.uniq.count != 2
  return answer
end
  
#################
def doubleton(num)
  until (num += 1).digits.group_by(&:itself).keys.count == 2; end; num
end
  
##########
def doubleton(num)
    n = num + 1
    while ((n.to_s).split("").uniq).length != 2
        n += 1
    end
    return n
end
