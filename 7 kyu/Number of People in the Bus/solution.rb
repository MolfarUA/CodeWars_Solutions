def number(bus_stops)
  bus_stops.map {|(on,off)| on - off }.reduce(:+)
end
_____________________________________
def number(bus_stops)
  passengers = 0
  bus_stops.each do |a,b|
    passengers += a - b
  end
  passengers
end
_____________________________________
def number(bus_stops)
  riders = 0
  bus_stops.each do |stop|
    riders += stop[0]
    riders -= stop[1]
  end
  return riders
end
_____________________________________
def number(arr)
  arr.map{|a,b| a - b }.sum
end
_____________________________________
def number(bus_stops)
  bus_stops.reduce(0) { |k, (on, off)| k + on - off }
end
_____________________________________
def number(bus_stops)
  
  return bus_stops.reduce(0) { |sum,stop| sum + (stop[0] - stop[1]) }
  
end
_____________________________________
def number(bus_stops)
  bus_stops.map { | i | i.reduce(:-) }.reduce(:+)
end
_____________________________________
def number(bus_stops)
  bus_stops.inject(0) { |count, (p_in, p_out)| count + p_in - p_out }
end
