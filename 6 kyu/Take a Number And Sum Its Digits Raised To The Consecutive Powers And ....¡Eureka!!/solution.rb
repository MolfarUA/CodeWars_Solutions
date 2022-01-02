def sum_dig_pow(a, b)
  (a...b).select { |n| n == n.to_s.chars.map.with_index(1) { |e, i| e.to_i ** i }.reduce(:+) }
end
_____________________________________________
def sum_dig_pow(a, b)
   (a..b).map {|x| eureka(x)}.compact
end

def eureka n
  n if (n.to_s.split('').map.with_index(1) {|item, index| item.to_i**index}.inject(:+) == n)
end
_____________________________________________
def sum_dig_pow(a, b)
  (a..b).select { |n|
    n == n.to_s.chars.each_with_index.inject(0) { |memo, (digit, index)| memo + digit.to_i ** (index + 1) }
  }
end
_____________________________________________
def sum_dig_pow(a, b)
  (a..b).select {|n| n.to_s.chars.map.with_index{|n, i| n.to_i**(i+1)}.reduce(:+) == n} 
end
_____________________________________________
def sum_dig_pow(a, b)
  (a..b).select { |n| eureka?(n) }
end

def eureka?(num)
  return false if num < 0
  num == num.to_s.chars.map.with_index(1) { |n, idx| n.to_i**idx }.reduce(0, :+)
end
_____________________________________________
def sum_dig_pow(a, b)
  [*a..b].select{|i|i==i.to_s.chars.map(&:to_i).each_with_index.reduce(0){|s,v|s+v[0]**(v[1]+1)}}
end
_____________________________________________
def sum_dig_pow(a, b)
  (a..b).select { |d| d.digits.reverse.each_with_index.reduce(0) {|memo, (el, i)| memo + el**(i + 1)} === d}
end
