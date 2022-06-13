def create_phone_number(arr)
  "(#{arr[0..2].join}) #{arr[3..5].join}-#{arr[6..9].join}"
end
_______________________________
def create_phone_number(arr)
  arr.join("").gsub(/^(.{3})(.{3})/, "(\\1) \\2-")
end
_______________________________
def create_phone_number(n)
  String.build do |io|
    io << "(" 
    io << n[0]
    io << n[1]
    io << n[2]
    io << ") "
    io << n[3]
    io << n[4]
    io << n[5]
    io << "-"
    io << n[6]
    io << n[7]
    io << n[8]
    io << n[9]
  end
end
_______________________________
def create_phone_number(arr)
  sprintf("(%d%d%d) %d%d%d-%d%d%d%d", arr)
end
_______________________________
def create_phone_number(arr)
  return "(#{arr[0..2].join}) #{arr.join[3..5]}-#{arr[6..9].join}"
end
_______________________________
def create_phone_number(a)
  "(#{a[0..2].join}) #{a[3..5].join}-#{a[6..-1].join}"
end
