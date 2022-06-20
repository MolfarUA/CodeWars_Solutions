55aa075506463dac6600010d


require 'set'

def list_squared(m, n)
  (m..n).map do |num|
    divisors = Set.new((1..Math.sqrt(num)).select { |d| num % d == 0 })
    divisors += divisors.map { |d| num / d } 

    sum_sq_divisors = divisors.map { |d| d * d }.inject(:+)
    [num, sum_sq_divisors] if Math.sqrt(sum_sq_divisors) % 1 == 0
  end.compact
end
________________________________
$arr = [[1, 1], [42, 2500], [246, 84100], [287, 84100], [728, 722500], [1434, 2856100], [1673, 2856100], [1880, 4884100], [4264, 24304900], [6237, 45024100], [9799, 96079204], [9855, 113635600]]

def list_squared(m, n)
  $arr.select { | i | i[0] >= m and i[0] <= n }
end
________________________________
def list_squared(m, n)
  result = []
  m.upto(n) do |num|
    devisors = Set.new
    1.upto(Math.sqrt(num)) do |d| 
      devisors << d**2 << (num / d)**2 if num % d == 0
    end
    sum = devisors.inject(0, :+)
    result << [num, sum] if Math.sqrt(sum) % 1== 0
  end
  return result
end
