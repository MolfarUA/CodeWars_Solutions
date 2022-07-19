55eea63119278d571d00006a


def next_id(arr)
  a = 0
  while arr.include?(a) 
    a += 1
  end
  a
    
end
______________________
def next_id(arr)
  ([*(0..arr.size)] - arr).min
end
______________________
def next_id(arr)
  (Array(0..arr.size) - arr)[0]
end
______________________
def next_id(arr)
  i = 0
  loop do
    return i unless arr.include?(i)
    i += 1
  end
end
