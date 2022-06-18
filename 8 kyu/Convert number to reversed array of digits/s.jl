digitize = digits
________________________
function digitize(n::Integer)::Array{Int64}
  reverse([parse(Int64, i) for i in string(n)])
end
________________________
function digitize(n)
  res = [parse(Int,x) for x in string(n)];
  return(reverse(res))
end
________________________
"""
Given a random non-negative number,
returns the digits of this number within an array in reverse order.
"""
function digitize(num)
  # alternatively collection() can be used instead of list creation with []
  return reverse([parse(Int, i) for i in string(num)], dims = 1)
end
