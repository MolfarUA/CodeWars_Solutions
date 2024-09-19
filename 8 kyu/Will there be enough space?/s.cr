5875b200d520904a04000003

def enough(cap, on, wait)
   [0, on + wait - cap].max
end 
_________________________
def enough(cap, on, wait)
  surplus = on + wait - cap
  surplus>0 ? surplus : 0
end 
_________________________
def enough(cap, on, wait)
  diff = cap - (on + wait)
  diff >= 0 ? 0 : -diff
end
_________________________
def enough(cap, on, wait)
  [on + wait - cap, 0].max
end 
