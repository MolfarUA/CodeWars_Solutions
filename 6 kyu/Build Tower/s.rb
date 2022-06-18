576757b1df89ecf5bd00073b


def towerBuilder(n)
  (1..n).map do |i|
    space = ' ' * (n - i)
    stars = '*' * (i * 2 - 1)
    space + stars + space
  end
end
_____________________________
def towerBuilder(n)
  n.times.map{|x|(?**(x*2+1)).center n*2-1}
end
_____________________________
def towerBuilder(n)
  Array.new(n){|k| (' ' * (n - k - 1)) + ('*' * (2 * k + 1)) + (' ' * (n - k - 1))}
end
_____________________________
def towerBuilder(n_floors)
  (1..n_floors).map { |i| ("*" * (i * 2 - 1)).center(n_floors * 2 - 1) }
end
_____________________________
def towerBuilder(n)
  arr = []
  1.upto(n) do |x|
    arr << ' '*(n - x) + '*'*(1 + 2*(x - 1)) + ' '*(n - x)
  end
  arr
end
_____________________________
def towerBuilder(n_floors)
  if n_floors > 1
    (0...n_floors).to_a.map do |i|
      "#{(' ') * (n_floors - i - 1)}*#{('*') * (i * 2)}#{(' ') * (n_floors - i - 1)}"
    end
  else
    ["*"]
  end
end
_____________________________
def towerBuilder(n_floors)
  steps = (2..n_floors).reduce([1]){|array, n| array << array.last + 2}
  max = steps.max

  steps.map do |step|
    ('*' * step).center(max) 
  end
end
