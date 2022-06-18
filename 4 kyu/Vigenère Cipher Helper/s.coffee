class VigenereCipher
  constructor: (@key, @abc) ->
  encode: (s) -> @cipher s, +1
  decode: (s) -> @cipher s, -1
  cipher: (text, mode) ->
    a = @abc.length; k = @key.length
    text.replace /./g, (c, i) => if (j = @abc.indexOf c) < 0
    then c else @abc[(j + mode * @abc.indexOf(@key[i % k])) %% a]
_____________________________________________
class VigenereCipher
  
  constructor: (@key, @abc) ->
    @alle = @abc.length
    @kele = @key.length
    
  encode: (str) ->
    output = ''
    for i of str
      char = str[i]
      code = @abc.indexOf char
      if code < 0
        output += char
      else
        output += @abc[(code + @abc.indexOf @key[i % @kele]) % @alle]
    output
    
  decode: (str) ->
    output = ''
    for i of str
      char = str[i]
      code = @abc.indexOf char
      if code < 0
        output += char
      else
        output += @abc[(code + @alle - @abc.indexOf @key[i % @kele]) % @alle]
    output
_____________________________________________
class VigenereCipher
  constructor: (@key, @abc) ->
  encode: (str) ->
    @map str, (c,i) =>
      return c if @abc.indexOf(c) == -1
      shift = @abc.indexOf(@key[i % @key.length])
      @abc[(@abc.indexOf(c) + shift) % @abc.length]
  decode: (str) ->
    @map str, (c, i) =>
      return c if @abc.indexOf(c) == -1
      index = (@abc.indexOf(c) - @abc.indexOf(@key[i % @key.length])) % @abc.length
      index = @abc.length + index if index < 0
      @abc[index]
  map: (str, fn) -> [].map.call(str, fn).join('')
_____________________________________________
class VigenereCipher
  constructor: (@key, @abc) -> @direction(1)
  direction: (@dir) ->
  transform: (letter,num) => 
      place = @abc.indexOf(letter)
      if place > -1
        @abc[(place + @abc.length + @dir * @abc.indexOf(@key[num % @key.length])) % @abc.length]
      else 
        letter
  encode: (str) ->
    @direction(1)
    str.split("").map(@transform).join ""
  decode: (str) ->
    @direction(-1)
    str.split("").map(@transform).join "" 
