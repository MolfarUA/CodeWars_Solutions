addBinary = (a,b) ->
  res=a+b
  ret=""
  fun=(a,b)->
    ret=res%2+ret
    res//=2
  fun a,b until res==0
  return ret
__________________________________
addBinary = (a,b) ->
    suma = a + b;
    return suma.toString(2);
__________________________________
addBinary = (a,b) -> return new Number(a + b).toString(2)
__________________________________
addBinary = (a,b) ->
  return (a+b).toString(2)
__________________________________
bin = (num) ->
  bits = (0 for _ in [0..Math.log2(num) | 0])
  while num
    if num == 1
      bits[0] = num--
      continue
    idx = Math.log2(num) | 0
    bits[idx] = 1
    num -= 2**idx
  return (bit + "" for bit in bits.reverse()).join("")

addBinary = (a,b) -> bin(a + b)
__________________________________
addBinary = (a,b) ->
  c = a + b
  c.toString(2)
