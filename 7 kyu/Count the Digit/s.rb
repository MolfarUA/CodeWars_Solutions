566fc12495810954b1000030


def nb_dig(n, d)
  (0..n).map { |k| k ** 2 }.join.count d.to_s
end
____________________________
def nb_dig(n, d)
  (0..n).inject(0){|count, i| count + (i**2).to_s.count(d.to_s) }
end
____________________________
def nb_dig(n, d)
  str = ""
  (0..n).each {|x| str += (x**2).to_s if (x**2).to_s.include? d.to_s }
  return str.count (d.to_s)
end
____________________________
def nb_dig(n, d)
  (0..n).map { |a| a*a }.join.scan(d.to_s).size
end
