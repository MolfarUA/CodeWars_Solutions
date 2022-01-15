Q = [
  '10'
  '11'
  '0110'
  '0111'
  '001100'
  '001101'
  '001110'
  '001111'
  '00011000'
  '00011001'
]

code = (s) ->
  s.split('').map((c) ->
    Q[c]
  ).join ''

decode = (q) ->
  p = new RegExp(Q.join('|'), 'g')
  q.replace p, (m) ->
    Q.indexOf m
__________________________
code = (strng) ->
  out = ''
  for n in strng.split('')
    bits = parseInt(n).toString 2
    out += '0'.repeat(bits.length - 1) + '1' + bits
  out

decode = (str) ->
  out = ''
  bits = ''
  bit_count = 0
  counting = yes
  
  for bit in str.split('')
    if counting
      if bit is '0'
        bit_count++
      else if bit is '1'
        counting = no
    else
      bits += bit
      if bit_count is 0
        out += parseInt(bits, 2).toString()
        bits = ''
      
        counting = yes
      else
        bit_count--
  out
__________________________
