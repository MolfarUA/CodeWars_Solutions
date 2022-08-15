52f677797c461daaf7000740


def solution(numbers)
  numbers.reduce { |a, b| a.gcd(b) } * numbers.size
end
_______________________________
def solution(arr)
  arr.reduce{|sum,n|gcd(sum,n)}  * arr.size
end

def gcd(a, b)
  b == 0 ? a : gcd(b, a % b)
end
_______________________________
def solution(numbers)
  min_val = numbers[0]
  arr = numbers.uniq
  n = arr.size
  (0..n-2).each do |i|
    (i+1..n-1).each do |j|
      r = arr[j].gcd arr[i]
      min_val = r if r < min_val
      return numbers.size if min_val == 1
    end
  end
  numbers.size * min_val
end
_______________________________
def solution(arr)
  a=arr[0]
  l=arr.size
  (1...l).each do |i|
    a=a.gcd(arr[i])
  end
  l*a
end
