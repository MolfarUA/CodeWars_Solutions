52f677797c461daaf7000740


def solution(n)
  n.reduce(:gcd) * n.size
end
_______________________________
def solution(numbers)
  numbers.inject(&:gcd) * numbers.length
end
_______________________________
def gcd(a,b) b>0 ? gcd(b,a%b) : a end; def solution(n) n.size*n.reduce{|a,b| a==1 ? 1 : gcd(a,b)} end
_______________________________
def solution(numbers)
   numbers.count * numbers.inject(:gcd);
end
_______________________________
def solution(numbers)
numbers.size * numbers.reduce(:gcd)
  end
