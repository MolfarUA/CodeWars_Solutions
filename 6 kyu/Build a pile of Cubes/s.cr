def find_nb(m : Int64)
  n = 1_i64
  while m > 0
    m = m - n**3
    n += 1
  end
  m == 0 ? n-1 : -1
end
_______________________________
def find_nb(m : Int64)
    n = 1_i64
    while m > 0
        m = m - n * n * n
        n += 1
    end
    m == 0 ? n - 1 : -1
end
_______________________________
def find_nb(m : Int64)
  n = Math.sqrt(2 * Math.sqrt(m)).floor
  n * n * (n + 1) * (n + 1) / 4 == m ? n : -1
end
_______________________________
def find_nb(m : Int64)
  r = Math.sqrt(0.25 + 2 * Math.sqrt(m)) - 0.5
  n = r.to_i
  return n if n == r
  -1
end
_______________________________
def find_nb(m : Int64) : Int32
  n = ((Math.sqrt(8 * Math.sqrt(m) + 1) - 1) / 2)
  (n%1).zero? ? n.to_i : -1
end
