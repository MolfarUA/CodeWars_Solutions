def doubleton(num)
  num += 1
  until num.digits.uniq.size == 2
    num += 1
  end
  num
end
______________
def doubleton(num)
  while true
    return num if (num += 1).to_s.chars.uniq.size == 2
  end
end
______________
def doubleton(num)
  while (num+=1).to_s.chars.to_set.size!=2; end
  num
end
__________
def doubleton(n)
  while (n=n+1).to_s.split("").to_set.size != 2 ; end
  n
end
________________
def doubleton(n : Int32)
  (n+1..1000000).each do |i|
      return i if (i.to_s.split("").uniq).size == 2
  end
end
______________
def doubleton(num)
  num +=1
  while num.to_s.chars.uniq.size != 2
    num += 1
  end
  num
end
