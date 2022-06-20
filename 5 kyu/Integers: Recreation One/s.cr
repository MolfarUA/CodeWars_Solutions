55aa075506463dac6600010d


def list_squared(m : Int64, n : Int64)
  (m..n).each_with_object([] of Array(Int32 | Int64)) do |i, obj|
    a = [] of Int32
    (1..i).each { |j| a.push j**2 if i % j == 0 }
    s = a.sum
    obj.push [i, s] if Math.sqrt(s) == Math.sqrt(s).to_i
  end
end
________________________________
C = [[1,1],[42,2500],[246,84100],[287,84100],[728,722500],[1434,2856100],[1673,2856100],[1880,4884100],
    [4264,24304900],[6237,45024100],[9799,96079204],[9855,113635600]]

def list_squared(m : Int64, n : Int64)
  C.select{|x| x[0] >= m && x[0] <= n}
end
________________________________
def list_squared(m : Int64, n : Int64)
  result = [] of Array(Int64)
  m.upto(n) do |i_i64|
    divisors = [] of Int64
    1_i64.upto(Math.sqrt(i_i64)) do |j_i64|
      if i_i64 % j_i64 == 0
        divisors << j_i64
        divisors << (i_i64 / j_i64) if j_i64 != i_i64 / j_i64
      end  
    end
    sum = divisors.map { |i_i64| i_i64 ** 2 }.reduce(0_i64){|m, e| m + e}
    sqr = Math.sqrt(sum)
    result << [i_i64, sum] if sqr.to_i.to_f == sqr
  end
  result
end
