def persistence(n)
  n < 10 ? 0 : 1 + persistence(n.to_s.chars.map(&:to_i).reduce(:*))
end
________________________________________
def persistence(n)
  return 0 if n < 10
  1 + persistence(n.digits.reduce(&:*))
end
________________________________________
def persistence(n)
  k = 0
   while n > 9 do
    n = n.to_s.split(//).map{|x| x.to_i}.inject(:*)
    k+=1
   end
  k 
end
________________________________________
def persistence(num)
  digits = num.digits
  counter = 0
  while digits.size > 1
    digits = digits.reduce(:*).digits
    counter += 1
  end
  counter
end
________________________________________
def persistence(num)
  if num < 10 then
    return 0
  else
    return 1 + persistence(num.to_s.chars.inject(1) { |n,c| n * c.to_i })
  end
end
