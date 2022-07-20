54d496788776e49e6b00052f


require "mathn"
def sumOfDivided(lst)
  factors = Hash.new(0)
  lst.each do |n|
    n.abs.prime_division.each do |p,_|
      factors[p] += n
    end
  end
  factors.sort
end
________________________________________________
require 'prime'

def sumOfDivided(lst)
  ret = []
  Prime.each(lst.map(&:abs).max) do |prime|
    nums = lst.select { |x| x % prime == 0 }
    next if nums.empty?
    ret << [prime, nums.reduce(:+)]
  end
  ret
end
________________________________________________
require 'prime'

def sumOfDivided(lst)
  factorized_list = []

  Prime.each(lst.map(&:abs).max) do |prime|
    multiples = lst.select { |x| is_divisible?(x, prime) }
    next if multiples.empty?
    factorized_list << [prime, multiples.reduce(:+)]
  end

  factorized_list
end

private
def is_divisible?(num, div) num % div == 0; end
