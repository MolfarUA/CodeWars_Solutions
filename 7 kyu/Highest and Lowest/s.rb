def high_and_low(numbers)
  numbers.split.map(&:to_i).minmax.reverse.join(' ')
end
______________________________
def high_and_low(numbers)
  numbers = numbers.split.map(&:to_i)
  "#{numbers.max} #{numbers.min}"
end
______________________________
def high_and_low(numbers)
  a = numbers.split.map(&:to_i).sort
  "#{a.last} #{a.first}"
end
______________________________
def high_and_low(numbers)
  delimiter = ' '
  
  numbers.
    split(delimiter).
    map {|i| i.to_i}.
    sort.
    values_at(-1, 0).
    join(delimiter)
end
______________________________
def high_and_low(numbers)
  numbers = numbers.split(' ')
  min = numbers[0].to_i
  max = numbers[0].to_i
  numbers.each do |x|
    min = x.to_i if min > x.to_i
    max = x.to_i if max < x.to_i
  end
  "#{max} #{min}"
end
