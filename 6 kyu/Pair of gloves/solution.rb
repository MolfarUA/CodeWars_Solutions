def number_of_pairs(gloves)
  gloves.uniq.map{|color|gloves.count(color)/2}.inject 0,:+
end

__________________
def number_of_pairs(g)
  g.group_by(&:itself).transform_values(&:size).values.map {|c| c / 2}.sum
end

___________
def number_of_pairs(gloves)
  gloves.each_with_object(Hash.new(0)) { |c, frq| frq[c] += 1 }.values.reduce(0) { |s, v|s += v/2 }
end

_______________
def number_of_pairs(gloves)
  gloves.group_by(&:itself).sum{|_,arr| arr.size/2}
end

_______________
def number_of_pairs(gloves)
  gloves.uniq.map{|e| gloves.count(e)/2}.sum
end

______________
def number_of_pairs(gloves)
  gloves.uniq.map { |glove| gloves.count(glove) / 2 }.sum
end

_____________
def number_of_pairs(gloves)
  gloves.uniq.inject(0) { |memo, color| memo + gloves.count(color) / 2 }
end

_____________
def number_of_pairs(gloves)
  pair = 0
  gloves.uniq.each{ |glove| pair += gloves.count(glove)/2 }
  return pair
end

_____________
def number_of_pairs(gloves)
  @gloves = gloves
  @gloves = (@gloves.uniq.map!{ |x| gloves.count(x) / 2 }).inject(:+)
  @gloves.to_i > 0 ? @gloves :  0
end
