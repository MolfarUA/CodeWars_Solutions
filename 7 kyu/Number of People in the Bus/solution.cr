def number(bus_stops)
  bus_stops.sum{ |(a, b)| a - b }
end
_____________________________________
def number(bus_stops)
  num_of_people = 0
  (0..bus_stops.size - 1).each do |index|
    num_of_people += bus_stops[index][0]
    num_of_people -= bus_stops[index][1]
  end
  num_of_people
end
_____________________________________
def number(bus_stops)
  bus_stops.sum{ |(on, off)| on - off }
end
_____________________________________
def number(bus_stops)
  bus_stops.sum{ |(i, o)| i - o }
end
