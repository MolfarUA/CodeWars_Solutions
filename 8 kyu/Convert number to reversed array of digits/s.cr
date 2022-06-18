def digitize(n)
  n.to_s.chars.reverse.map {|x| x.to_i}
end
________________________
def digitize(n)
  n.to_s.chars.map do | i |
    i.to_i
  end.reverse
end
________________________
def digitize(n)
  n.to_s.split("").reverse.map &.to_i
end
________________________
def digitize(n : Number) : Array(Int32)
  n.to_s
   .split("")
   .reverse
   .map{ |n| n.to_i }
end
________________________
def digitize(n)
  n.to_s.reverse.chars.map &.to_i
end
________________________
def digitize(n)
  if n==0
    return [0]
  end;
  arr = [] of typeof(n);
  while n != 0
    arr<<n%10;
    n/=10;
  end;
  return arr;
end;
