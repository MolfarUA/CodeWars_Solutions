586beb5ba44cfc44ed0006c3


def sum_even_numbers(q)
  q.select{|i| i % 2 == 0}.sum  
end
_______________________________________
def sum_even_numbers(seq)
  seq.select {|x| x % 2 == 0}.sum
end
_______________________________________
def sum_even_numbers(seq)
  numbers = seq.select { |n| n % 2 == 0 }
  return numbers.sum
end
