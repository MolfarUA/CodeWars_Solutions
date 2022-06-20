58e230e5e24dde0996000070


require 'prime'

def next_prime(n)
  (n + 1).step.find(&:prime?)
end
__________________________
require 'prime'

def next_prime(n)
  (n + 1).step { |i| return i if i.prime? }
end
__________________________
require 'prime'

def next_prime(n)
  return 2 if n < 2
  (n + 1..10**12).detect{ |i| Prime.prime?(i) }
end
