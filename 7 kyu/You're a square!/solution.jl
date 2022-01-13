issquare(n) = n ≥ 0 && isinteger(√n)
__________________________________
function issquare(n)
  n ≥ 0 && isinteger(√n)
end
__________________________________
function issquare(n)
  n>=0 ? floor(√n) == √n : false 
end
__________________________________
function issquare(n)
  if n < 0
    return false
  end
  mod(sqrt(n), 1) == 0 ? true : false
end
__________________________________
function issquare(n)
  return floor(sqrt(abs(BigInt(n))))^2 == n
end
