def multiply(a, b)
  a*b
end 
###########
def multiply(a,b)
  raise ArgumentError, 'arguments must be a numbers' unless a.is_a?(Integer) and b.is_a?(Integer)
  a*b
end
#######
def multiply *nums
  nums.reduce(:*)
end
###########
def multiply(n1,n2)
  return n1 * n2
end

puts multiply(3,2)
##########
def multiply(*n)
  n.reduce(:*)
end
###########
def multiply(a = 0, b = 0)
    raise ArgumentError, 'Arguments must be a numbers' unless a.is_a?(Numeric) and b.is_a?(Numeric)
    a*b
end
#########
def multiply(*a)
  a.inject(1, &:*)
end
