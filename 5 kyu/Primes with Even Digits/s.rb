require 'prime'

def f(n)
  Prime.each(n-1).max_by { |i| [i.digits.count(&:even?), i] }
end
____________________________________________
require 'prime'

def f(target)
  Prime.take_while { |n| n < target }.reverse.max_by { |n| n.digits.count(&:even?) }
end
____________________________________________
require "prime"

$primes_with_even_digits = []
max_even_digits = 1

Prime.each(5000000) { |p|
  even_digits = p.to_s.count("02468")
  $primes_with_even_digits << p if even_digits >= max_even_digits
  max_even_digits = even_digits if even_digits > max_even_digits
}

$primes_with_even_digits.reverse!

def f(n)
  $primes_with_even_digits.bsearch { |x| x < n}
end
____________________________________________
def primes_less_than_n(n) 
  p = (0..n-1).to_a 
  p[0] = nil 
  p[1] = nil 
  i = 2 
  while i**2 < n 
    j = 2 
    while i*j < n 
      p[i*j] = nil 
      j += 1 
    end
    i += 1 
  end
  p.compact.reverse
end

def f(n) 
  len = n.to_s.length 
  primes = primes_less_than_n(n)
  i = 0 
  while i < primes.length 
    if primes[i].to_s.chars.count {|int| int.to_i.even?} == len - 1 
      return primes[i]
    end
    i += 1 
  end
  i = 0 
  while i < primes.length 
    if primes[i].to_s.chars.count {|int| int.to_i.even?} == len - 2 
      return primes_less_than_n(n)[i]
    end
    i += 1 
  end
end
____________________________________________
def f(n)
  res = []
  Prime.each(n-1) { |prime| res << prime }
  res.sort_by { |num| num.to_s.count("02468") }.last
end
____________________________________________
require 'prime'
def f n
  Prime.take_while{|pr|pr < n}.group_by{|pr|pr.to_s.scan(/[24680]/).size}.max.last.max
end
____________________________________________
require 'prime'

$primes = []
if $primes.size == 0
  Prime.each(1000000) do |p|
    $primes << p
  end
end

$nb_even = []
$primes.each do |p|
  a = p.to_s.split('')
  a.keep_if{|x| x.to_i % 2 == 0}
  $nb_even << a.count
end

def f(n)
  my_prime   = $primes.reject {|x| x > n-1}
  my_nb_even = $nb_even[0..my_prime.size-1]
  my_max     = my_nb_even.max
  i = my_nb_even.map.with_index {|a, i| a ==  my_max ? i : nil}.compact.last
  return $primes[i]
end
