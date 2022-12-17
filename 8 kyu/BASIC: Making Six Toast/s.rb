5834fec22fb0ba7d080000e8


def six_toast(num) 
  (6-num).abs
end
________________________
def six_toast(num) 
  (num-6).abs
end
________________________
def six_toast(num) 
  if num > 5 
    return num -6
  else
    return num
  end
end
