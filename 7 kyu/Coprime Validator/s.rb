def coprime?(n, m)
  n.gcd(m) == 1
end
___________________________
def coprime?(n, m)
  nf = (1..n).select { |x| n % x == 0 }
  mf = (1..m).select { |y| m % y == 0 }
  nf.select { |z| mf.include?(z) }.max == 1
end
___________________________
def coprime?(n, m)
  factors(n) & factors(m) == [1]
end

def factors(n)
  (1..n).select { |i| n % i == 0 }  
end
___________________________
def coprime?(n, m)
  (2..m).each do |num|
    if n % num == 0 && m % num == 0
      return false
    end
  end
true
end
___________________________
def coprime?(n, m)
  def divisors(num)
    (2..num).select {|x| num % x == 0}
  end
  
  !(divisors(n) & divisors(m)).any?
  
end
