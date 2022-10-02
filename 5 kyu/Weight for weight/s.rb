55c6126177c9441a570000cc


def order_weight(string)
  string.split.sort_by { |n| [n.chars.map(&:to_i).reduce(:+), n] }.join(" ")
end
______________________________
def weight(str)
  str.to_s.chars.map(&:to_i).reduce(:+)
end

def order_weight(str)
  str.split.sort { |a,b| [weight(a),a] <=> [weight(b),b] }.join(" ")
end
______________________________
def order_weight(strng)
    (strng.split.sort.sort_by {|x| x.to_i.digits.sum}).join(" ")
end
