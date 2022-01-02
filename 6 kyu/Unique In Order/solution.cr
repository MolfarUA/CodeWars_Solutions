def unique_in_order(element : String)
  unique_in_order element.split("").reject(&.empty?)
end

def unique_in_order(element : Array)
  res = element.class.new
  last = nil
  element.each do |c|
    res << c if c != last
    last = c
  end
  res
end
_____________________________________________
def unique_in_order(vals)
  if vals.is_a? String
    vals.chars.chunk(&.itself).map(&.first.to_s).to_a
  else
    vals.chunk(&.itself).map(&.first).to_a
  end
end
_____________________________________________
def unique_in_order(a, fix = false)
  return unique_in_order(a.chars, true) if a.is_a?(String)
  return [] of Int32 if a.size == 0
  xs = Array(typeof(a[0])).new
  prev = nil
  a.each{|e|
    xs << e if prev != e
    prev = e
  }
  xs.map{|e| fix && e.is_a?(Char) ? e.to_s : e}
end
_____________________________________________
def unique_in_order(element : Enumerable)
  element.chunks(&.itself).map(&.first)
end

def unique_in_order(element : String)
  element.squeeze.split("", remove_empty: true)
end
_____________________________________________
def unique_in_order(element : Enumerable)
  element.chunks(&.itself).map(&.first)
end

def unique_in_order(element : String)
  element.squeeze.chars.map(&.to_s)
end
_____________________________________________
def u(l : Array(T)) forall T
  r = [] of T
  l.each { |e| r << e unless r[-1]? == e }; r
end

def unique_in_order(x)
  return u(x.chars.map(&.to_s)) if x.is_a?(String)
  u(x)
end
_____________________________________________
def unique_in_order(element)
  if element.is_a? String
    if element.empty?
      return [] of String
    end
    element = element.split ""
  else
    return element if element.empty?
  end
  r = [element[0]]
  element[1..].each do |v|
    if v != r.last
      r << v
    end
  end
  r
end
