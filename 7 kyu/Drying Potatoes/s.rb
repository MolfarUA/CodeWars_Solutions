def potatoes(p0, w0, p1)
  w0 * (100 - p0) / (100 - p1)
end
_______________________________________________
def potatoes(p0, w0, p1)
    (w0.to_f * (100.0 - p0.to_f) / (100.0 - p1.to_f)).to_i
end
_______________________________________________
def potatoes(p0, w0, p1)
    return w0 * (100 - p0) / (100 - p1)
end
_______________________________________________
def potatoes(p0, w0, p1)
    result = ''  
    if p0.is_a?(Integer) && p0 >= 0 && w0.is_a?(Integer) && w0 >= 0 && p1.is_a?(Integer) && p1 >= 0  
      result = (w0 * (100-p0)/(100-p1))  
    end
    result
end
_______________________________________________
def potatoes(p0, w0, p1)
  (w0 * (100 - p0)) / (100 - p1)
end

# full potato weight (water + dry) = 100
# water percentage = 99
# end water percentage = 98
# final potato weight (water + dry) = 50
# 100 * .99 = water
# 100 * (1-.99) = dry
# water * end / start = final water
# dry + final water
