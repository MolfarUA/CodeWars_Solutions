55df87b23ed27f40b90001e5


def calc(t,i)
  l,n,o = 0,t,t.to_s(i)
  while true
    l = n*t+l/i
    n = l%i
    o = n.to_s(i)+o
    break if l==t
  end
  o[1..o.length]
end
____________________________
def calc(trailing, base)
  digit = trailing
  carryover = 0
  number_from_end = ''
  loop do
    number_from_end << digit.to_s(base)
    prov = digit * trailing + carryover
    return number_from_end.reverse if prov == trailing
    carryover = prov / base
    digit = prov % base
  end
end
____________________________
def calc(l, b)
  digits = [l]
  carry = 0
  loop do
    x = digits.last*l + carry
    carry, r = x.divmod b
    break if r == l and carry == 0
    digits.push r
  end

  digits.reverse
    .collect {|d| d.to_s(b).upcase}
    .join
end
