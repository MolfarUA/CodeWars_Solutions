56484848ba95170a8000004d


def gps(s, x)
  return 0 if x.size <= 1
  x.each_cons(2).map { |a, b| ((b - a) / s) * 3600 }.max.floor
end
_____________________________
def gps(s, x) 
  x.each_cons(2).map { |c| (60 * (60.0 / s) * (c[1] - c[0])) }.max.to_i.round(1)
end
_____________________________
def gps(seconds, array)
  result = []
  (array.length - 1).times do |ind|
    result << (array[ind + 1] - array[ind]) / seconds
  end
  result.max * 60 * 60 rescue 0
end
_____________________________
def gps s, x
    x.map.with_index{|d, i|  (3600 * (i == 0 ? 0 : d - x[i-1])) / s}.max&.floor || 0
end
