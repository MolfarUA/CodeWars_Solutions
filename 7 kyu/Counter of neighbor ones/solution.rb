def ones_counter(input)
  input.join.scan(/1+/).map(&:size)
end
_____________________________________________
def ones_counter(input)
  input.chunk {|x| x == 1}.select {|p, x| p}.map {|p, x| x.size}
end
_____________________________________________
def ones_counter(input)
 input.join.split('0').reject(&:empty?).map(&:length)
end
_____________________________________________
def ones_counter(input)
  input.chunk(&:itself).reject { |x,y| x.zero? }.each_with_object([]) { |v, arr| arr << v.last.size }
end
_____________________________________________
def ones_counter(input) input.chunk_while{|a, b| a==b}.map(&:sum)-[0] end
_____________________________________________
def ones_counter(input)
  res = []
  if !input.include?(1) 
    return res
  end
  
  sum = 0
  input.each{ |x|
    if !input.include?(0)
     return [input.sum]
    elsif x == 1 
      sum += 1
    else
      if sum > 0
        res << sum
        sum = 0
      end
    end
      }
  if sum > 0
    res << sum
  end
    res
end
