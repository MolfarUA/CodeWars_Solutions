55e7d9d63bdc3caa2500007d


def smallest(n)
  (1..n).inject(:lcm)
end
________________________________
def smallest(n)
  (1..n).reduce(:lcm)
end
________________________________
def smallest(n)
  return n if n <= 2

  def lcm a, b
    a * b / gcd(a, b)
  end

  def gcd a, b
    a, b = [a, b].minmax
    until b % a == 0
      a, b = b % a, a
    end
    a
  end

  return lcm(smallest(n-1), n)
end
________________________________
require 'prime'

def smallest(n)
  return 1 if n == 1
  primes = Prime.first(15).select{ |p| p <= n }
  pows = primes.map { |p|  Math.log(n, p).floor }
  primes.zip(pows).reduce(1) {|s, e| s *= (e[0]**e[1])}
end
