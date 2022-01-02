def number(bus_stops):
    nr_of_people = 0
    for t in bus_stops:
        nr_of_people += t[0]
        nr_of_people -= t[1]
    
    return nr_of_people
_____________________________________
def number(bus_stops):
    return sum([stop[0] - stop[1] for stop in bus_stops])
_____________________________________
def number(stops):
    return sum(i - o for i, o in stops)
_____________________________________
def number(bus_stops):
    return sum(on - off for on, off in bus_stops)
_____________________________________
def number(bus_stops):
    bus = 0
    stop = 0
    for i in bus_stops:
        bus += i[0]
        stop += i[1]
    return(bus - stop)
_____________________________________
def number(bus_stops):
    new_list = []
    for a, b in bus_stops:
        new_list.append(a - b)
    return(sum(new_list))
_____________________________________
def number(bs):
    inside = 0
    
    for stop in range(len(bs)):
        get_in = bs[stop][0]
        get_off = bs[stop][1]
        inside = inside + get_in - get_off
        
    return inside
_____________________________________
def number(bus_stops):
    return sum(p_in[0] for p_in in bus_stops) - sum(p_out[1] for p_out in bus_stops)
  
_____________________________________
def number(bus_stops):
    r=0
    for i,j in bus_stops:
        r+=i
        r-=j
    if r<0:
        r=0
    return r
