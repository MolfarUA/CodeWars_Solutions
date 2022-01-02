def unique_in_order(iterable)
  (iterable.is_a?(String) ? iterable.chars : iterable).chunk { |x| x }.map(&:first)
end
_____________________________________________
def unique_in_order(iterable)
  it_array= []
  iterable.length.times do |x|
    it_array << iterable[x] if iterable[x] != iterable[x+1]
  end
  it_array
end
_____________________________________________
def unique_in_order(iterable)
  iterable = iterable.chars if iterable.is_a?(String)
  answer = []
  iterable.each do |el|
    answer << el if answer.last != el
  end
  answer
end
_____________________________________________
def unique_in_order(iterable)
  case iterable
    when String
      iterable.gsub(/(.)\1*/, '\1').split('')
    when Array
      iterable.uniq
  end
end
_____________________________________________
def unique_in_order(iterable)
  iterable.is_a?(String) ? (iterable = iterable.chars) : iterable
  
  unique = []
  iterable.each do |element|
    unique << element if unique.last != element
  end
  unique
end
