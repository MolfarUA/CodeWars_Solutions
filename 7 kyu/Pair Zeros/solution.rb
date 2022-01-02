def pair_zeros(arr)
  arr.join.gsub(/0(.*?)0/, '0\1').chars.map(&:to_i)
end
_____________________________________
def pair_zeros(arr)
  skip = true
  arr.reject{|el| el == 0 && skip = !skip}
end
_____________________________________
def pair_zeros a, t=nil
  a.select{|x|x!=0||t=!t}
end
_____________________________________
def pair_zeros(arr)
  zero = false
  arr.select {|n| n.zero? ? zero = !zero : true }
end
_____________________________________
def pair_zeros(arr)
  arr.join.gsub(/(0)([1-9]*)(0)/,'\1\2').chars.map(&:to_i)
end
_____________________________________
def pair_zeros(arr)
  pair = false
  result = []
  
  arr.each { |n|
    if n.zero? && pair
      pair = false
    else
      pair = true if n.zero?
      result << n
    end
  }
  
  result
end
