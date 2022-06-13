def find_nb(m)
  ct = 0
  while m > 0
    ct += 1
    m -= ct**3
  end
  m == 0 ? ct : -1
end
_________________________________________
def find_nb(m)
  n = ((m * 4)**0.25).to_i
  (n**2) * ((n + 1)**2) / 4 == m ? n : -1
end
_________________________________________
def find_nb(m)
  check = Math.sqrt(2* Math.sqrt(m)).floor
  (check * (check + 1)/2)**2 == m ? check : -1
end
_________________________________________
def find_nb(m)
  r = Integer ((m ** 0.5 * 2)**0.5)
  (r * (r + 1) / 2)**2 == m ? r : -1
end
_________________________________________
def find_nb(m)
  n = 1
  sum = 1
  while sum < m
   n += 1
   sum += n**3
  end
return sum == m ? n : -1
end
