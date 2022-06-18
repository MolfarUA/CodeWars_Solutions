595bbea8a930ac0b91000130

def calculate_1RM(w, r)
  return case r
    when 0 then 0
    when 1 then w
    else [
      w * (1 + r / 30.0),               # Epley
      100 * w / (101.3 - 2.67123 * r),  # McGlothin
      w * r**0.10                       # Lombardi
      ].max.round
    end
  end
_______________________________
def calculate_1RM(w,r)
  return w if r == 1
  return 0 if r == 0
  [w*(1.+r.fdiv(30)),100*w/(101.3-2.67123*r),w*r**0.1].max.round
end
_______________________________
def calculate_1RM(w, r)
  return 0 if r == 0
  return w if r == 1
  
  [
    epley(w, r),
    mcglothin(w, r),
    lombardi(w, r)
  ].map(&:round).max
end

def epley(w, r)
  w * (1 + r.fdiv(30))
end

def mcglothin(w, r)
  (100 * w).fdiv(101.3 - 2.67123*r)
end

def lombardi(w, r)
  w * r**0.1
end
_______________________________
def calculate_1RM(w,r)
  return 0 if r.zero?
  return w if r == 1  
  [w*(1+(r/30.0)), (100*w)/(101.3 - 2.67123 * r), (w * r ** 0.1)].max.round
end
