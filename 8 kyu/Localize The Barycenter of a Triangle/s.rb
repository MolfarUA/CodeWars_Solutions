5601c5f6ba804403c7000004


def bar_triang(*verts)
  [median(verts,0), median(verts,1)]
end

def median(coords, i)
  (coords.map{|c| c[i]}.reduce(&:+)/3.0).round(4)
end
__________________________________
def bar_triang(*points)
  points.transpose.map{|x| (x.inject(:+).to_f/3).round(4) }
end
__________________________________
def bar_triang(p1, p2, p3)
  p1.zip(p2, p3).map { |n| n.reduce(:+).fdiv(3).round(4) }
end
__________________________________
def bar_triang(p1,p2,p3)
  x = (p1[0] + p2[0] + p3[0]) / 3.0
  y = (p1[1] + p2[1] + p3[1]) / 3.0
  [x.round(4),y.round(4)]
end
