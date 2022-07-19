561e9c843a2ef5a40c0000a4


require 'prime'

def gap(gap, low, high)
  primes_between(low,high).each_cons(2).find { |(a,b)| b-a == gap }
end

def primes_between(low,high)
  Prime.each(high).select { |prime| prime >= low }
end
__________________________________
require 'prime'

def gap(g,m,n)
  Prime.take_while { |i| i<=n }.reject { |i| i<m }.each_cons(2).find { |a,b| b-a == g }
end
__________________________________
require 'prime'
def gap(g, m, n)
  Prime.each(n).select { |p| p >= m }.each_cons(2).find { |a, b| b - a == g }
end
__________________________________
require 'prime'

def gap(g, m, n)
  prime = Hash.new { |h, k| h[k] = k.prime? }
  primes_in = -> (rng) { rng.any? { |n| prime[n] } }
  p = (m...n).find() { |a| prime[a] && !primes_in.call(a+1...a+g) && prime[a+g] }
  p ? [p, p + g] : nil
end
