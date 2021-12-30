def digital_root(n : Int64)
   n == 0 ? 0: n % 9 == 0 ? 9: n % 9
end

________________________________
def digital_root(n : Int64)
  (n - 1).remainder(9) + 1
end

________________________________
def digital_root(n : Int64)
  while n > 9
    n = n.to_s.chars.map{|c|c.to_i}.sum
  end
  n
end

________________________________
def digital_root(n : Int64)
  loop do
    break if n < 10
    n = n.to_s.split("").map(&.to_i).sum
  end
  n
end

________________________________
def digital_root(n : Int64)
  n < 10 ? n : digital_root(n.to_s.chars.reduce(0.to_i64) { |s, c| s + c.to_i })
end

________________________________
def digital_root(n : Int64)
  until n < 10
    n = n.digits.sum
  end
  n
end
