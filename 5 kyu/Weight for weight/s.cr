55c6126177c9441a570000cc


def order_weight(ws)
  ws.split.sort_by!{ |w| {w.each_char.map(&.to_i).sum, w} }.join(' ')
end
_____________________________
def d_sum(n)
  n.to_s.chars.map{|x| x.to_i}.reduce(0){|m, e| m + e}
end
def comp(a, b)
  cp = d_sum(a) - d_sum(b)
  if (cp == 0) 
    return a <=> b 
  end
  cp < 0 ? -1 : 1
end
def order_weight(ws)
  ws.split.sort { |x, y| comp(x, y) }.join(" ")
end
_____________________________
def order_weight(ws)
  ws.split.sort_by!{ |v| {v.each_char.sum(&.to_i), v} }.join(' ')
end
_____________________________
def order_weight(ws)
  ws.split(' ').sort_by{ |v| {v.chars.sum(&.to_i), v} }.join(' ')
end
