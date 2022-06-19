544aed4c4a30184e960010f4


def divisors(n)
  vals = (2..n/2).select{|x| n%x==0}
  vals.empty? ? "#{n} is prime" : vals
end
__________________________________
require 'prime'
def divisors(n)
  n.prime? ? "#{n} is prime" : (2...n).select{|i|n%i==0}
end
__________________________________
def divisors(n)
  divisors = (2...n).select{|item| n % item == 0}
  divisors.empty? ? "#{n} is prime" : divisors
end
__________________________________
def divisors(n)
  return nil if n < 2 
  divs = (2...n).select {|k| n % k == 0}
  divs.empty? ? "#{n} is prime" : divs
end
__________________________________
def divisors(n)
  require 'prime'
  arr = []
  if Prime.prime?(n) == true
    return "#{n} is prime"
  else
    (1+1...n).map { |y| arr.push(y) if n % y ==0  }
    return arr
  end
end
