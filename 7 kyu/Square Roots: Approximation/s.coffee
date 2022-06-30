58475cce273e5560f40000fa


approxRoot = (n) ->
  lowPsq = Math.floor(Math.sqrt(n));
  highPsq = Math.ceil(Math.sqrt(n));
  if (lowPsq == highPsq) 
    return lowPsq;
  res = lowPsq + ((n - lowPsq**2) / (highPsq**2 - lowPsq**2));  
  return +res.toFixed(2);
____________________________
approxRoot = (n) ->
  if Math.sqrt(n) % 1 == 0
    return Math.sqrt(n)
  ss = Math.pow(~~(Math.sqrt(n)), 2)
  ls = Math.pow(Math.ceil(Math.sqrt(n)), 2)
  return +((Math.sqrt(ss) + ((n - ss) / (ls - ss))).toFixed(2)) 
