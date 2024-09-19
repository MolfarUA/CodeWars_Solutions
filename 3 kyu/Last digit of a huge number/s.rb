def last_digit(lst)
  n = 1

  # the ones digit is at most a 4 cycle for any a^b
  # therefor (a ^ b) % 10 == (a ^ (b % 4)) % 10
  # special case when b is non-zero and divisible by 4, we should use 4 instead
  
  # x1 ^ (x2 ^ (x3 ^ x4)) % 10 
  # let a = x1
  #     b = x2 ^ (x3 ^ x4)
  #
  # a ^ b % 10 == a ^ (b % 4) % 10
  #
  # b % 4 = x2 ^ (x3 ^ x4) % 4 = (x2 ^ (x3 ^ x4) % 4) % 10
  # continue ...

  lst.reverse.each do |x|
    power = n < 4 ? n : n % 4 + 4
    n = x ** power
  end
  
  n % 10
end
_________________________
def last_digit(lst)
  return 1 if lst.length == 0
  n, over = 1, false
  lst.reverse[...-1].each do |p|
    r = p & 3
    next_over = ((n > 1 and p > 1) or (n == 1 and p > 3) or (over and p > 1))
    n = n != 0 ? (
      r == 2 ? (
        n > 1 || over ? 0 : n == 1 ? 2 : 1
      ) : n & 1 != 0 ? r : r != 0 ? 1 : 0
    ) : over ? r & 1 : 1
    over = next_over
  end
  (lst[0] % 10) ** (over ? n + 4 : n) % 10
end
________________________
def last_digit(lst)
  p lst
n = 1
lst.reverse.each do |w|
   n = w ** (n < 4 ? n : n % 4 + 4)
end
n % 10
end
______________
def last_digit(xs)
  xs.reverse.inject(1) { |a, x| (x < 20 ? x : x % 20 + 20) ** (a < 4 ? a : a % 4 + 4) } % 10
end
