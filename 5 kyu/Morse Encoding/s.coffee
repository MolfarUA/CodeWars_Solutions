536602df5d0266e7b0000d31


String::padEnd?=(a,b)->(@+Array(+a+1).join b)[...a]
String::padStart?=(a,b)->(Array(+a+1).join(b)+@)[-a..]
String::map?=(f)->[].map.call @,f

Morse =
  encode: (m)->
    m.map((c)->morse[c] ?0).join('000').match /.{1,32}/g
    .map (a)->a=a.padEnd 32,'0';(parseInt(a[...-1],2)<<1)+ +a[31]

  decode: (m) ->
    m.map (a)->((a>>>1).toString(2)+(a&1)).padStart 32,'0'
    .join('').split('0000000').join('000 000').split '000'
    .map (a)->parse[a] ?' '
    .join('').trim()

morse={}; parse={}
'0531|1515|257|353|451|550|6516|7524|8528|9530|A21|B48|C410|D34|E10|F42|G36|H40|I20|J47|K35|L44|M23|N22|O37|P46|Q413|R32|S30|T11|U31|V41|W33|X49|Y411|Z412|.621|,651|?612|\'630|!643|/518|(522|)645|&58|:656|;642|=517|+510|-633|_613|"618|$79|@626'
.split('|').map (a)->
  [k,l]=a
  m=(+a[2..]).toString(2).padStart l,'0'
  .map((c)->['1','111'][c]).join '0'
  morse[k]=m
  parse[m]=k
________________________________________________
Morse = {};

Morse.encode = (message) ->
  array = [integerIndex = 0]
  for letter in message
    for bit in Morse.alpha[letter] + '000'
      array.push integerIndex = 0 if integerIndex > 31
      array[array.length - 1] |= +bit << 31 - integerIndex++
  array

Morse.invert_alpha = ->
  unless Morse._invert_alpha
    Morse._invert_alpha = {}
    for key, value of Morse.alpha
      Morse._invert_alpha[value] = key
  Morse._invert_alpha  

Morse.decode = (integerArray) ->
  message = ''
  character = ''
  for integer, n in integerArray
    i = 31
    for i in [31..0]
      character += (integer >> i) & 1
      if n is integerArray.length - 1 and (integer << (31 - i + 1)) is 0
        return message + Morse.invert_alpha()[character]
      if character.length > 3 and
      character[character.length - 3] is '0' and
      character[character.length - 2] is '0' and
      character[character.length - 1] is '0'
        message += Morse.invert_alpha()[character[0..-4]]
        character = ''
  message

Morse.alpha = {
  'A': '10111',
  'B': '111010101',
  'C': '11101011101',
  'D': '1110101',
  'E': '1',
  'F': '101011101',
  'G': '111011101',
  'H': '1010101',
  'I': '101',
  'J': '1011101110111',
  'K': '111010111',
  'L': '101110101',
  'M': '1110111',
  'N': '11101',
  'O': '11101110111',
  'P': '10111011101',
  'Q': '1110111010111',
  'R': '1011101',
  'S': '10101',
  'T': '111',
  'U': '1010111',
  'V': '101010111',
  'W': '101110111',
  'X': '11101010111',
  'Y': '1110101110111',
  'Z': '11101110101',
  '0': '1110111011101110111',
  '1': '10111011101110111',
  '2': '101011101110111',
  '3': '1010101110111',
  '4': '10101010111',
  '5': '101010101',
  '6': '11101010101',
  '7': '1110111010101',
  '8': '111011101110101',
  '9': '11101110111011101',
  '.': '10111010111010111',
  ',': '1110111010101110111',
  '?': '101011101110101',
  "'": '1011101110111011101',
  '!': '1110101110101110111',
  '/': '1110101011101',
  '(': '111010111011101',
  ')': '1110101110111010111',
  '&': '10111010101',
  ':': '11101110111010101',
  ';': '11101011101011101',
  '=': '1110101010111',
  '+': '1011101011101',
  '-': '111010101010111',
  '_': '10101110111010111',
  '"': '101110101011101',
  '$': '10101011101010111',
  '@': '10111011101011101',
  ' ': '0' # Technically is 7 0-bits, but we assume that a space will always be between two other characters
};
________________________________________________
Morse = {}

Morse.encode = (msg) ->
  words = msg.split(' ')
  bin = words.map((word) ->
    Array.from(word).map((c) ->
      Morse.alpha[c]
    ).join '000'
  ).join('0000000')
  encoded = bin.padEnd(Math.ceil(bin.length / 32) * 32, '0').match(/.{32}/g).map((chunk) ->
    -(~parseInt(chunk, 2) + 1)
  )
  encoded

Morse.decode = (array) ->
  bin = array.map((n) ->
    (if n < 0 then 2 ** 32 + n else n).toString(2).padStart 32, '0'
  ).join('').replace(/0+$/, '')
  decoded = bin.split('0000000').map((word) ->
    word.split('000').map((s) ->
      Object.keys(Morse.alpha).find (k) ->
        Morse.alpha[k] == s
    ).join ''
  ).join(' ')
  decoded

Morse.alpha = {
  'A': '10111',
  'B': '111010101',
  'C': '11101011101',
  'D': '1110101',
  'E': '1',
  'F': '101011101',
  'G': '111011101',
  'H': '1010101',
  'I': '101',
  'J': '1011101110111',
  'K': '111010111',
  'L': '101110101',
  'M': '1110111',
  'N': '11101',
  'O': '11101110111',
  'P': '10111011101',
  'Q': '1110111010111',
  'R': '1011101',
  'S': '10101',
  'T': '111',
  'U': '1010111',
  'V': '101010111',
  'W': '101110111',
  'X': '11101010111',
  'Y': '1110101110111',
  'Z': '11101110101',
  '0': '1110111011101110111',
  '1': '10111011101110111',
  '2': '101011101110111',
  '3': '1010101110111',
  '4': '10101010111',
  '5': '101010101',
  '6': '11101010101',
  '7': '1110111010101',
  '8': '111011101110101',
  '9': '11101110111011101',
  '.': '10111010111010111',
  ',': '1110111010101110111',
  '?': '101011101110101',
  "'": '1011101110111011101',
  '!': '1110101110101110111',
  '/': '1110101011101',
  '(': '111010111011101',
  ')': '1110101110111010111',
  '&': '10111010101',
  ':': '11101110111010101',
  ';': '11101011101011101',
  '=': '1110101010111',
  '+': '1011101011101',
  '-': '111010101010111',
  '_': '10101110111010111',
  '"': '101110101011101',
  '$': '10101011101010111',
  '@': '10111011101011101',
  ' ': '0'
}
________________________________________________
Morse = {};

Morse.encode = (message) ->
  bits = message.split("").map((c) -> Morse.alpha[c]).join("000")
  padded = (bits + "0".repeat(31 - (bits.length - 1) % 32)).match(/[01]{32}/g)
  padded.map((val) -> parseInt(val, 2) | 0);

Morse.decode = (intArr) ->
  bits = intArr.map((val) ->
    temp = (val %% 4294967296).toString(2)
    "0".repeat(31 - (temp.length - 1) % 32) + temp
  )
  trimmed = bits.join("").replace(/0/g, " ").trim().replace(/ /g, "0")
  reverse = {}
  for c of Morse.alpha then reverse[Morse.alpha[c]] = c
  chars = trimmed.split("0000000").map((word) -> word.split("000").map((ch) -> reverse[ch]).join("")).join(" ")

Morse.alpha = {
  'A': '10111',
  'B': '111010101',
  'C': '11101011101',
  'D': '1110101',
  'E': '1',
  'F': '101011101',
  'G': '111011101',
  'H': '1010101',
  'I': '101',
  'J': '1011101110111',
  'K': '111010111',
  'L': '101110101',
  'M': '1110111',
  'N': '11101',
  'O': '11101110111',
  'P': '10111011101',
  'Q': '1110111010111',
  'R': '1011101',
  'S': '10101',
  'T': '111',
  'U': '1010111',
  'V': '101010111',
  'W': '101110111',
  'X': '11101010111',
  'Y': '1110101110111',
  'Z': '11101110101',
  '0': '1110111011101110111',
  '1': '10111011101110111',
  '2': '101011101110111',
  '3': '1010101110111',
  '4': '10101010111',
  '5': '101010101',
  '6': '11101010101',
  '7': '1110111010101',
  '8': '111011101110101',
  '9': '11101110111011101',
  '.': '10111010111010111',
  ',': '1110111010101110111',
  '?': '101011101110101',
  "'": '1011101110111011101',
  '!': '1110101110101110111',
  '/': '1110101011101',
  '(': '111010111011101',
  ')': '1110101110111010111',
  '&': '10111010101',
  ':': '11101110111010101',
  ';': '11101011101011101',
  '=': '1110101010111',
  '+': '1011101011101',
  '-': '111010101010111',
  '_': '10101110111010111',
  '"': '101110101011101',
  '$': '10101011101010111',
  '@': '10111011101011101',
  ' ': '0' # Technically is 7 0-bits, but we assume that a space will always be between two other characters
};
________________________________________________
Morse = {};

Morse.encode = (message) ->
  alpha = Morse.alpha
  bit_pattern = message.split('').map((name) -> alpha[name]).join('000')
  bit_pattern += '0' for i in [1..32 - bit_pattern.length % 32]
  bit_values = []
  bit_values.push bit_pattern.slice(32 * i, (i + 1) * 32) for i in [0...bit_pattern.length/32]
  result = []
  for bit_value in bit_values
    number = parseInt(bit_value, 2)
    result.push if bit_value.charAt(0) == "1" then -~number - 1 else number
  result

Morse.decode = (integerArray) ->
  bits = []
  for integer, index in integerArray
    add = ''
    if integer < 0
      bit = (-integer - 1).toString(2)
      bit = bit.replace(/\d/g, (str) -> if str == '1' then 0 else '1')
      for i in [1..32 - bit.length]
        add += '1'
    else
      bit = integer.toString(2)
      for i in [0...32 - bit.length]
        add += '0'
    bit = add + bit
    bits.push bit

  symbols = bits.join('')
    .replace(/0*$/, '') 
    .replace(/0000000/g, '000 000')
    .split('000')
    .map((symbol) -> if symbol == ' ' then '0' else symbol)

  new_alpha = {}
  for key, value of Morse.alpha
    new_alpha[value] = key
  
  result = []
  for symbol in symbols
    result.push new_alpha[symbol]
  result.join('')

Morse.alpha = {
  'A': '10111',
  'B': '111010101',
  'C': '11101011101',
  'D': '1110101',
  'E': '1',
  'F': '101011101',
  'G': '111011101',
  'H': '1010101',
  'I': '101',
  'J': '1011101110111',
  'K': '111010111',
  'L': '101110101',
  'M': '1110111',
  'N': '11101',
  'O': '11101110111',
  'P': '10111011101',
  'Q': '1110111010111',
  'R': '1011101',
  'S': '10101',
  'T': '111',
  'U': '1010111',
  'V': '101010111',
  'W': '101110111',
  'X': '11101010111',
  'Y': '1110101110111',
  'Z': '11101110101',
  '0': '1110111011101110111',
  '1': '10111011101110111',
  '2': '101011101110111',
  '3': '1010101110111',
  '4': '10101010111',
  '5': '101010101',
  '6': '11101010101',
  '7': '1110111010101',
  '8': '111011101110101',
  '9': '11101110111011101',
  '.': '10111010111010111',
  ',': '1110111010101110111',
  '?': '101011101110101',
  "'": '1011101110111011101',
  '!': '1110101110101110111',
  '/': '1110101011101',
  '(': '111010111011101',
  ')': '1110101110111010111',
  '&': '10111010101',
  ':': '11101110111010101',
  ';': '11101011101011101',
  '=': '1110101010111',
  '+': '1011101011101',
  '-': '111010101010111',
  '_': '10101110111010111',
  '"': '101110101011101',
  '$': '10101011101010111',
  '@': '10111011101011101',
  ' ': '0' # Technically is 7 0-bits, but we assume that a space will always be between two other characters
};
