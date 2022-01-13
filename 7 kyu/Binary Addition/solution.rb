def add_binary(a,b)
  (a + b).to_s(2)
end
__________________________________
def add_binary(a,b)
  sum = a + b
  "#{sum.to_s(2)}"
end
__________________________________
def add_binary(a,b)
p = a + b
return p.to_s(2) 
end
__________________________________
def add_binary(a,b)
  num = a + b
  rest = 0
  result = []
  
  if (num == 1) 
    return '1';
  end
  if (num == 0)
    return '0';
  end
  
  while(num > 1)
    rest = num%2
    num = num/2
    result << rest
  end  

  result << 1
  return result.reverse.join
end
