def powers_of_two(n)
  (0..n).map { |k| 2**k }
end
___________________________________
def powers_of_two(n)
  (0..n).map {|el| 2**el}

end
___________________________________
def powers_of_two(n)
  (1+n).times.map{|x|2**x}
end
___________________________________
def powers_of_two(n)
  (0..n).map{|i| 2**i}
end
___________________________________
def powers_of_two(n)
  arr = [1]
  i = 2
  j = 1
  while j <= n do
    arr << i ** j
    j += 1
  end
  return arr
end
