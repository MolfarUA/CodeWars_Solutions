55caf1fd8063ddfa8e000018


def arithmetic_sequence_elements(a,r,n)
  Array.new(n) { |n| r*n+a }.join(", ")
end
___________________________
def arithmetic_sequence_elements(a,r,n)
  a.step(by: r).take(n).join ', '
end
___________________________
def arithmetic_sequence_elements(a, r, n)
  a.step(by: r).first(n).join(", ")
end
