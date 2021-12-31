def hamming(n)
  @nums ||= (0..45).to_a.repeated_permutation(3).map { |e| 2**e[0] * 3 ** e[1] * 5 ** e[2] }.sort.take(5000)
  @nums[n-1]
end

___________________________________________________
def hamming(n)
  result = [1]
  i = j = k = 0
  while result.size < n
    result << [result[i]*2,result[j]*3,result[k]*5].min
    i += 1 if result.last == result[i] * 2
    j += 1 if result.last == result[j] * 3
    k += 1 if result.last == result[k] * 5
  end
  result.last
end

___________________________________________________
require 'set'

module Hamming
  @@cache = {
    next_hammings: SortedSet[2, 3, 5],
    hammings: {
      1 => 1
    }
  }
  
  def self.next_hamming
    res = @@cache[:next_hammings].to_a.first

    @@cache[:next_hammings].delete(res)
    @@cache[:next_hammings].merge([res*2, res*3, res*5])

    res
  end
  
  def self.smallest_hamming(n)    
    (@@cache[:hammings].keys.max..n).each { |i| @@cache[:hammings][i] ||= next_hamming }

    @@cache[:hammings][n]
  end
end

def hamming(n)
  Hamming.smallest_hamming(n)
end

___________________________________________________
@keys = []

def hamming(n)
  
  return 1 if n == 1
  

  if @keys.empty?

    h = Hash.new(1)

    0.upto(81) do |i|
      0.upto(81) do |j|
        0.upto(81) do |k|
          # p "#{i}  #{j} #{k}"
          h[hamm(i, j, k)] = 1
        end
      end
    end
    @keys = h.keys.sort
    
  end


  @keys[n-1]  

end

def hamm(i, j, k)
  (2 ** i) * (3 ** j) * (5 ** k)
end

___________________________________________________
def hamming(n)
  h = [1]
  m = [2,3,5]
  x = [2,3,5]
  i = [0,0,0]
  (1...n).each do |index|
    h[index] = x.min
    3.times do |p|
      if h[index] == x[p]
        i[p] += 1
        x[p] = m[p] * h[i[p]]
      end
    end
  end
  h[n-1]
end
