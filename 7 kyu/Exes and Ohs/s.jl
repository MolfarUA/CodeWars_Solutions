function xo(str)
  count(c in "Xx" for c in str) == count(c in "Oo" for c in str)
end
__________________________________
function xo(str)
  count(==('x'), lowercase(str)) == count(==('o'), lowercase(str))
end
__________________________________
function xo(str)
    count(i,str) = length(findall(isequal(i), lowercase(str)))
    count('x',str) == count('o',str)
end
__________________________________
function xo(str)
  x = 0
  o = 0
  for char in str
    if lowercase(char) == 'x'
      x += 1
    elseif lowercase(char) == 'o'
      o += 1
    end
  end
  
  return x == o
end
__________________________________
function xo(str)
  count(q->lowercase(q)=='x',str) == count(q->lowercase(q)=='o',str)
end
