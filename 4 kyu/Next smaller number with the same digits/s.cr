5659c6d896bc135c4c00021e


def next_smaller(n : Int64)
  d = n.to_s.chars.map{|c|c.to_i}
  x = y = -1
  (0..d.size-2).reverse_each{|i|
    break if x > -1
    (i+1...d.size).each{|j|
      if d[j]<d[i]
        x = i
        break
      end
    }
  }
  return x if x == -1
  (x+1...d.size).each{|i|
    y = i if d[i] < d[x] && (y == -1 || d[i] > d[y])
  }
  return -1 if d[y] == 0 && x == 0
  t = d[x]
  d[x] = d[y]
  d[y] = t
  e = d[x+1...d.size].sort{|a,b| b <=> a}
  j = 0
  (x+1...d.size).each{|i|
    d[i] = e[j]
    j += 1
  }
  d.join("").to_i64
end
_______________________________
def next_smaller(n : Int64)
  if n<10
    return -1
  end
  m,r=n.divmod(10)
  until m==0
    d=m%10
    if d>r
      break
    else
      m/=10
      r=d
    end
  end
  if m==0
    return -1
  end
  s=n.to_s.chars
  l=s.size
  j=l-1
  i=j
  until s[i-1]>s[i]
    i-=1
  end
  until s[j]<s[i-1]
    j-=1
  end
  tmp=s[i-1]
  s[i-1]=s[j]
  s[j]=tmp
  s[0]=='0' ? -1 : (s[0..i-1].join+(l-1).downto(i).map{|k| s[k]}.join).to_i64
end
_______________________________
def next_smaller(n : Int64)
digits = n.to_s.chars.reverse.map(&.to_i64)
  return -1 if digits.sort.join == n.to_s  
  digits[0..-2].each.with_index(1_i8) do | digit, i |
    if digits[i] > digit
      head = digits[0..i].sort
      ordered = head.select { | d | d < digits[i] }
      head << head.delete_at(ordered.size-1)
      result = head + digits[i+1..-1]
      return -1 if result.last.zero?
      return result.reverse.join.to_i64
    end
  end
end
