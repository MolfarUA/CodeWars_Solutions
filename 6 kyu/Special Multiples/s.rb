55e785dfcb59864f200000d9


require 'prime'
def count_specMult(n, m)
  (m - 1) / Prime.first(n).reduce(&:*)
end
_________________________________
require "prime"

def count_specMult(n, limit)
   (limit - 1) / Prime.first(n).reduce(&:*)
end
_________________________________
require "prime"
def count_specMult(n,maxVal)
  primes = Prime.first(n).reduce(:*)
  return (maxVal - 1) / primes
end
