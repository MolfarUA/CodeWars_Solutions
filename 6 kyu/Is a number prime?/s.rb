require 'prime'

def isPrime(num)
  num.prime?
end
___________________
require 'prime'

# Ruby naming conventions - *all* methods should use snake_case and predicate names should end in a "?"
def is_prime? n
  Prime.prime? n
end

# Just to pass the Kata
def isPrime n; is_prime? n; end
_____________________
require "prime"

define_method :isPrime, &:prime?
