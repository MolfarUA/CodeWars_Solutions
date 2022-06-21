5545f109004975ea66000086


def is_divisible(n,x,y)
  (n % x == 0) && (n % y == 0)
end
_____________________
def is_divisible(n, *divisors)
  divisors.all? { |div| n % div == 0 }
end
_____________________
def is_divisible(n,x,y)
  n % x == 0 && n % y == 0 ? true : false
end
