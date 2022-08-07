55caf1fd8063ddfa8e000018


def arithmetic_sequence_elements(a,r,n)
  (0...n).map{|x| x * r + a}.join(", ")
end
___________________________
def arithmetic_sequence_elements(a,r,n)
  res = [a]
  (n-1).times do
    res << res.last + r
  end
  res.join(", ")
end
___________________________
def arithmetic_sequence_elements(a, d, n)
  (0...n).map { |i| a + i * d }.join(", ")
end
