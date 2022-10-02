5547cc7dcad755e480000004


def removNb(n)
  # sum = n * (n + 1) / 2
  # fn = -> x { [(sum - x) / ( x + 1 ),  (sum - x) % (x + 1)] }

  # (1..n).reduce([]) do |result, x|
  #   y, reminder = fn.(x)
  #   reminder == 0 && y < n ?  result << [x, y] : result
  # end
  Solver.new(n).call
end

class Solver
  def initialize(n)
    @border = n
    @sum = n * (n + 1) / 2
  end
  
  def call
    (1..border - 1).reduce([]) do |result, x|
      y, reminder = y_with_reminder(x) 
      reminder == 0 && y < border ? result << [x, y] : result
    end
  end
  
  private
  
  attr_reader :border, :sum
  
  def y_with_reminder(x)
    [(sum - x) / (x + 1), (sum - x) % (x + 1)]
  end
end
______________________________
# generate a range from 1 to n
# use an iterator/each over the range we generated to get our first number
# nest an iterator over range move the number up to get every possible number of pairs
# while inside second iterator, we are going to remove the two numbers from the array
# sum the resulting number test for equality under two numbers
# append to some sort of results array

# total = (n*n + n) /2
# (total - a - b) = ab
# (total - a) = ab + b = b(a+1) 
# ((total - a) / (a+1)) = b


def removNb(n)
  res = []
  total = (n*n + n) / 2
  range = (1..n)
  
  (1..n).each do |a|
    b = ((total - a) / (a * 1.0 + 1.0))
    if b == b.to_i && b <= n
      res.push([a,b.to_i])
      
    end
  end
 
  
  return res
end
