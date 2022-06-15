def averages(arr)
  (0..arr.size-2).map{|i| (arr[i] + arr[i+1])/2.0} rescue []
end
____________________________
def averages(arr)
  arr.each_cons(2).map { |x,y| (x+y).fdiv(2) } rescue []
end
____________________________
class Array
  def mean
    self.reduce(:+)/self.length.to_f
  end
end
def averages(arr)
  arr.each_cons(2).to_a.map(&:mean)
rescue 
  []
end
____________________________
def averages(arr)
  arr&.each_cons(2)&.map { |a, b| (a + b) / 2.0 } || []
end
____________________________
def averages(arr)
  Array(arr).each_cons(2).map { |pair| pair.sum.fdiv(2) }
end
