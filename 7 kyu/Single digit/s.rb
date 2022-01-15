def single_digit(n)
  n < 10 ? n : single_digit(n.to_s(2).count('1'))
end
__________________________
def single_digit(n)
  n = n.digits(2).sum until n < 10
  n
end
__________________________
def single_digit(n)
  while n.to_s.length > 1
    sum = 0
    n.to_s(2).chars.each do |num|
      sum += num.to_i
    end
    n = sum
  end
  n
end
__________________________
def single_digit(n)
  if n < 10
    n
  elsif
    num = n.to_s(2).to_i.digits.sum
    if num >= 10
      num2 = num.to_s(2).to_i.digits.sum
      return num2
    else 
      return num
    end
  end
    
end
__________________________
def single_digit(n)
  while  n > 9
    n = n.to_s(2).scan(/1/).length
  end
  n
end
__________________________
def single_digit(n)
  return n if n < 10
  begin
    n = n.digits(2).sum
  end while n > 9
  n
end
