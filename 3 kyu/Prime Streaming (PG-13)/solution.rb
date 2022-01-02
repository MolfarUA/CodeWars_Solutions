class Primes
  # generate primes using half-sieve
  @PRIMES = [2]
  LIMIT = 10**6 * 16
  
  SIEVE = [true] * (LIMIT/2)
  SIEVE[0] = nil
  SIEVE.each.with_index { |is_prime, x|
    if is_prime
      x = x*2 + 1
      @PRIMES << x
      (x*x..LIMIT).step(x*2) { |i| SIEVE[i/2] = nil }
    end
  }
  SIEVE = nil
  
  
  def self.stream
    @PRIMES.each
  end
end
___________________________________________________________
class Primes
  
  def initialize
    @i = 0
  end  
  
  def self.get_primes
    max = 15487000
    result = [2]
    sieve = []
    number = 3
    while number < max
      if !sieve[number]
        result << number
        number_2 = 2 * number
        k = number_2 + number
        while k < max
          sieve[k] = true
          k += number_2
        end  
      end  
      number += 2
    end
    result
  end  
  
  def self.stream
    @@numbers ||= get_primes
    self.new
  end
  
  def next
    @i += 1
    @@numbers[@i-1]
  end  
end
___________________________________________________________
class Integer
  @@known_primes = [2, 3]
  @@sieve = [true, true, false, false]
  @@limit = 3

  def primes_to
    return if self <= @@limit 
    sieve = @@sieve
    known_primes = @@known_primes
    
    known_primes.each do | prime | 
      ([@@limit / prime, prime].max .. self / prime).each do | f |
        sieve[f * prime] = true
      end
    end
    
    k = (@@limit + 1) | 1
    while k**2 < self
      k += 2
      next if sieve[k]
      known_primes << k
      ([@@limit / k, k].max .. self / k).each do | f |
        sieve[f * k] = true
      end
    end

    @@limit = self
    (k..@@limit).each do | i |
      known_primes << i unless sieve[i]
    end
  end
  
  def prime_at
    while true
      return @@known_primes[self] if @@known_primes[self]
      (@@limit * 2).primes_to 
    end
  end
end


class Primes
  def self.stream
    Enumerator.new do |y|
      idx = 0
      loop do
        y << prime = idx.prime_at
        idx += 1
      end
    end
  end
end


class Primes
  def self.stream
    Enumerator.new do |y|
      idx = 0
      loop do
        y << prime = idx.prime_at
        idx += 1
      end
    end
  end
end
___________________________________________________________
max = 16e6.to_i
$primes = (0..max).to_a
  $primes[0] = $primes[1] = nil
  counter = 0
  $primes.each do |p|
    next unless p
    break if p*p > max
    counter += 1
    (p*p).step(max,p) { |m| $primes[m] = nil }
  end

class Primes
  def self.stream
    Enumerator.new do |enum|
      i = 3
      enum.yield 2
      while true
        enum.yield i if $primes[i] != nil
        i += 2
      end
    end
  end
end
